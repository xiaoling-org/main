/**
 * 应用状态管理
 */

import React, {createContext, useContext, useReducer, ReactNode} from 'react';
import {createStore} from 'zustand';
import {persist, createJSONStorage} from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {Board, Task, Tag, User, SyncData} from '@/types';

// 应用状态
interface AppState {
  // 用户
  user: User | null;
  token: string | null;
  
  // 数据
  boards: Board[];
  currentBoardId: string | null;
  tags: Tag[];
  
  // UI状态
  isLoading: boolean;
  error: string | null;
  
  // 同步状态
  lastSync: string | null;
  isSyncing: boolean;
  offlineChanges: any[];
  
  // Actions
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  setBoards: (boards: Board[]) => void;
  setCurrentBoard: (boardId: string | null) => void;
  setTags: (tags: Tag[]) => void;
  addTask: (task: Task) => void;
  updateTask: (taskId: string, updates: Partial<Task>) => void;
  moveTask: (taskId: string, fromColumnId: string, toColumnId: string, index: number) => void;
  deleteTask: (taskId: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  syncData: (data: SyncData) => void;
  addOfflineChange: (change: any) => void;
  clearOfflineChanges: () => void;
  reset: () => void;
}

// 创建Zustand store
const useAppStore = createStore<AppState>()(
  persist(
    (set, get) => ({
      // 初始状态
      user: null,
      token: null,
      boards: [],
      currentBoardId: null,
      tags: [],
      isLoading: false,
      error: null,
      lastSync: null,
      isSyncing: false,
      offlineChanges: [],
      
      // Actions
      setUser: (user) => set({user}),
      setToken: (token) => set({token}),
      setBoards: (boards) => set({boards}),
      setCurrentBoard: (boardId) => set({currentBoardId: boardId}),
      setTags: (tags) => set({tags}),
      
      addTask: (task) => {
        const {boards, currentBoardId} = get();
        const updatedBoards = boards.map(board => {
          if (board.id === currentBoardId) {
            const updatedColumns = board.columns.map(column => {
              if (column.id === task.columnId) {
                return {
                  ...column,
                  tasks: [...column.tasks, task],
                };
              }
              return column;
            });
            return {...board, columns: updatedColumns};
          }
          return board;
        });
        set({boards: updatedBoards});
      },
      
      updateTask: (taskId, updates) => {
        const {boards} = get();
        const updatedBoards = boards.map(board => ({
          ...board,
          columns: board.columns.map(column => ({
            ...column,
            tasks: column.tasks.map(task =>
              task.id === taskId ? {...task, ...updates, updatedAt: new Date().toISOString()} : task
            ),
          })),
        }));
        set({boards: updatedBoards});
      },
      
      moveTask: (taskId, fromColumnId, toColumnId, index) => {
        const {boards, currentBoardId} = get();
        const updatedBoards = boards.map(board => {
          if (board.id === currentBoardId) {
            let movedTask: Task | null = null;
            
            // 从原列移除
            const columnsWithRemoved = board.columns.map(column => {
              if (column.id === fromColumnId) {
                const taskIndex = column.tasks.findIndex(t => t.id === taskId);
                if (taskIndex !== -1) {
                  movedTask = column.tasks[taskIndex];
                  return {
                    ...column,
                    tasks: column.tasks.filter((_, i) => i !== taskIndex),
                  };
                }
              }
              return column;
            });
            
            // 添加到目标列
            const finalColumns = columnsWithRemoved.map(column => {
              if (column.id === toColumnId && movedTask) {
                const updatedTask = {
                  ...movedTask,
                  columnId: toColumnId,
                  updatedAt: new Date().toISOString(),
                };
                const newTasks = [...column.tasks];
                newTasks.splice(index, 0, updatedTask);
                return {...column, tasks: newTasks};
              }
              return column;
            });
            
            return {...board, columns: finalColumns};
          }
          return board;
        });
        set({boards: updatedBoards});
      },
      
      deleteTask: (taskId) => {
        const {boards} = get();
        const updatedBoards = boards.map(board => ({
          ...board,
          columns: board.columns.map(column => ({
            ...column,
            tasks: column.tasks.filter(task => task.id !== taskId),
          })),
        }));
        set({boards: updatedBoards});
      },
      
      setLoading: (loading) => set({isLoading: loading}),
      setError: (error) => set({error}),
      
      syncData: (data) => {
        set({
          boards: data.boards,
          tags: data.tags,
          lastSync: data.lastSync,
          isSyncing: false,
        });
      },
      
      addOfflineChange: (change) => {
        set(state => ({
          offlineChanges: [...state.offlineChanges, change],
        }));
      },
      
      clearOfflineChanges: () => set({offlineChanges: []}),
      
      reset: () => {
        set({
          user: null,
          token: null,
          boards: [],
          currentBoardId: null,
          tags: [],
          isLoading: false,
          error: null,
          lastSync: null,
          isSyncing: false,
          offlineChanges: [],
        });
      },
    }),
    {
      name: 'kanban-storage',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        boards: state.boards,
        currentBoardId: state.currentBoardId,
        tags: state.tags,
        lastSync: state.lastSync,
      }),
    }
  )
);

// React Context Provider
const StoreContext = createContext<typeof useAppStore | null>(null);

interface StoreProviderProps {
  children: ReactNode;
}

export const StoreProvider: React.FC<StoreProviderProps> = ({children}) => {
  return (
    <StoreContext.Provider value={useAppStore}>
      {children}
    </StoreContext.Provider>
  );
};

// Hook to use the store
export const useStore = () => {
  const store = useContext(StoreContext);
  if (!store) {
    throw new Error('useStore must be used within StoreProvider');
  }
  return store;
};

export default useAppStore;