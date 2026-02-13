/**
 * 看板页面 - 核心拖拽功能
 */

import React, {useState, useCallback} from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  Dimensions,
  ScrollView,
} from 'react-native';
import {Appbar, Card, Button, FAB, Portal, Modal} from 'react-native-paper';
import DraggableFlatList from 'react-native-draggable-flatlist';
import {GestureHandlerRootView} from 'react-native-gesture-handler';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import {useNavigation, useRoute} from '@react-navigation/native';
import {useStore} from '@/store';
import {Column, Task} from '@/types';

const {width} = Dimensions.get('window');
const COLUMN_WIDTH = width * 0.85;

const BoardScreen: React.FC = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const store = useStore();
  const {boards, moveTask} = store();

  const [activeColumn, setActiveColumn] = useState<string | null>(null);
  const [showAddTask, setShowAddTask] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');

  // 获取当前看板
  const boardId = (route.params as any)?.boardId || 'default';
  const board = boards.find(b => b.id === boardId) || boards[0];
  const columns = board?.columns || [];

  // 处理任务拖拽
  const handleTaskDragEnd = useCallback(
    (columnId: string, tasks: Task[]) => {
      // 更新本地状态
      const updatedBoards = boards.map(b => {
        if (b.id === boardId) {
          const updatedColumns = b.columns.map(col => {
            if (col.id === columnId) {
              return {...col, tasks};
            }
            return col;
          });
          return {...b, columns: updatedColumns};
        }
        return b;
      });

      // 更新store
      store.setState({boards: updatedBoards});
    },
    [boardId, boards, store],
  );

  // 添加新任务
  const handleAddTask = () => {
    if (!newTaskTitle.trim() || !activeColumn) return;

    const newTask: Task = {
      id: Date.now().toString(),
      title: newTaskTitle,
      columnId: activeColumn,
      boardId: boardId,
      priority: 'medium',
      tags: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    // 更新store
    const updatedBoards = boards.map(b => {
      if (b.id === boardId) {
        const updatedColumns = b.columns.map(col => {
          if (col.id === activeColumn) {
            return {...col, tasks: [...col.tasks, newTask]};
          }
          return col;
        });
        return {...b, columns: updatedColumns};
      }
      return b;
    });

    store.setState({boards: updatedBoards});
    setNewTaskTitle('');
    setShowAddTask(false);
  };

  // 渲染任务卡片
  const renderTaskCard = ({item, drag, isActive}: {item: Task; drag: any; isActive: boolean}) => {
    const priorityColors = {
      low: '#4CAF50',
      medium: '#FF9800',
      high: '#F44336',
      urgent: '#9C27B0',
    };

    return (
      <Card
        style={[
          styles.taskCard,
          isActive && styles.activeTaskCard,
        ]}
        onLongPress={drag}
        onPress={() => navigation.navigate('Task', {taskId: item.id} as never)}>
        <Card.Content>
          <View style={styles.taskHeader}>
            <Text style={styles.taskTitle} numberOfLines={2}>
              {item.title}
            </Text>
            <View
              style={[
                styles.priorityDot,
                {backgroundColor: priorityColors[item.priority]},
              ]}
            />
          </View>

          {item.description && (
            <Text style={styles.taskDescription} numberOfLines={2}>
              {item.description}
            </Text>
          )}

          {item.tags && item.tags.length > 0 && (
            <View style={styles.tagsContainer}>
              {item.tags.slice(0, 3).map((tag, index) => (
                <View key={index} style={styles.tag}>
                  <Text style={styles.tagText}>#{tag}</Text>
                </View>
              ))}
              {item.tags.length > 3 && (
                <Text style={styles.moreTags}>+{item.tags.length - 3}</Text>
              )}
            </View>
          )}

          <View style={styles.taskFooter}>
            {item.dueDate && (
              <View style={styles.dueDate}>
                <Icon name="calendar" size={12} color="#666" />
                <Text style={styles.dueDateText}>
                  {new Date(item.dueDate).toLocaleDateString()}
                </Text>
              </View>
            )}

            <View style={styles.taskStats}>
              {item.comments && item.comments.length > 0 && (
                <View style={styles.stat}>
                  <Icon name="comment" size={12} color="#666" />
                  <Text style={styles.statText}>{item.comments.length}</Text>
                </View>
              )}
              {item.attachments && item.attachments.length > 0 && (
                <View style={styles.stat}>
                  <Icon name="paperclip" size={12} color="#666" />
                  <Text style={styles.statText}>{item.attachments.length}</Text>
                </View>
              )}
            </View>
          </View>
        </Card.Content>
      </Card>
    );
  };

  // 渲染看板列
  const renderColumn = (column: Column, index: number) => {
    const columnColors = {
      todo: '#FFEBEE',
      doing: '#FFF3E0',
      done: '#E8F5E9',
    };

    const columnColor = columnColors[column.id as keyof typeof columnColors] || '#F5F5F5';

    return (
      <View key={column.id} style={styles.column}>
        <View style={[styles.columnHeader, {backgroundColor: columnColor}]}>
          <Text style={styles.columnTitle}>{column.name}</Text>
          <Text style={styles.columnCount}>{column.tasks.length}</Text>
        </View>

        <GestureHandlerRootView style={styles.columnContent}>
          <DraggableFlatList
            data={column.tasks}
            keyExtractor={item => item.id}
            renderItem={renderTaskCard}
            onDragEnd={({data}) => handleTaskDragEnd(column.id, data)}
            activationDistance={10}
            containerStyle={styles.dragListContainer}
            contentContainerStyle={styles.dragListContent}
          />
        </GestureHandlerRootView>

        <Button
          mode="text"
          style={styles.addTaskButton}
          onPress={() => {
            setActiveColumn(column.id);
            setShowAddTask(true);
          }}>
          <Icon name="plus" size={20} />
          <Text>添加任务</Text>
        </Button>
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <Appbar.Header>
        <Appbar.BackAction onPress={() => navigation.goBack()} />
        <Appbar.Content title={board?.name || '看板'} />
        <Appbar.Action icon="magnify" onPress={() => {}} />
        <Appbar.Action icon="dots-vertical" onPress={() => {}} />
      </Appbar.Header>

      <ScrollView
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        style={styles.boardScroll}
        contentContainerStyle={styles.boardContent}>
        {columns.map(renderColumn)}
      </ScrollView>

      {/* 添加任务模态框 */}
      <Portal>
        <Modal
          visible={showAddTask}
          onDismiss={() => setShowAddTask(false)}
          contentContainerStyle={styles.modalContainer}>
          <Card>
            <Card.Title
              title="添加新任务"
              subtitle={columns.find(c => c.id === activeColumn)?.name}
            />
            <Card.Content>
              <TextInput
                label="任务标题"
                value={newTaskTitle}
                onChangeText={setNewTaskTitle}
                mode="outlined"
                style={styles.input}
                autoFocus
              />
            </Card.Content>
            <Card.Actions>
              <Button onPress={() => setShowAddTask(false)}>取消</Button>
              <Button mode="contained" onPress={handleAddTask}>
                添加
              </Button>
            </Card.Actions>
          </Card>
        </Modal>
      </Portal>

      {/* 全局操作按钮 */}
      <FAB
        style={styles.fab}
        icon="plus"
        onPress={() => {
          setActiveColumn(columns[0]?.id || null);
          setShowAddTask(true);
        }}
      />
    </SafeAreaView>
  );
};

// 需要导入TextInput
import {TextInput} from 'react-native-paper';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  boardScroll: {
    flex: 1,
  },
  boardContent: {
    paddingHorizontal: 8,
  },
  column: {
    width: COLUMN_WIDTH,
    marginHorizontal: 8,
    backgroundColor: '#fff',
    borderRadius: 12,
    elevation: 2,
    overflow: 'hidden',
  },
  columnHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0,0,0,0.1)',
  },
  columnTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  columnCount: {
    fontSize: 14,
    fontWeight: '500',
    color: '#666',
    backgroundColor: 'rgba(255,255,255,0.8)',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
  },
  columnContent: {
    flex: 1,
    minHeight: 400,
  },
  dragListContainer: {
    flex: 1,
  },
  dragListContent: {
    padding: 8,
  },
  taskCard: {
    marginBottom: 8,
    elevation: 1,
  },
  activeTaskCard: {
    elevation: 8,
    transform: [{scale: 1.02}],
  },
  taskHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  taskTitle: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
    flex: 1,
    marginRight: 8,
  },
  priorityDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginTop: 4,
  },
  taskDescription: {
    fontSize: 12,
    color: '#666',
    marginBottom: 8,
    lineHeight: 16,
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 8,
  },
  tag: {
    backgroundColor: '#E3F2FD',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
    marginRight: 4,
    marginBottom: 4,
  },
  tagText: {
    fontSize: 10,
    color: '#1976D2',
  },
  moreTags: {
    fontSize: 10,
    color: '#666',
    alignSelf: 'center',
    marginLeft: 4,
  },
  taskFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  dueDate: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  dueDateText: {
    fontSize: 10,
    color: '#666',
    marginLeft: 4,
  },
  taskStats: {
    flexDirection: 'row',
  },
  stat: {
    flexDirection: 'row',
    alignItems: 'center',
    marginLeft: 8,
  },
  statText: {
    fontSize: 10,
    color: '#666',
    marginLeft: 2,
  },
  addTaskButton: {
    borderTopWidth: 1,
    borderTopColor: '#F0F0F0',
    marginTop: 8,
  },
  modalContainer: {
    padding: 20,
  },
  input: {
    marginBottom: 16,
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: '#2196F3',
  },
});

export default BoardScreen;