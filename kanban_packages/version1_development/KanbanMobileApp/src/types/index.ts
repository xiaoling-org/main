/**
 * 应用类型定义
 */

// 任务优先级
export type TaskPriority = 'low' | 'medium' | 'high' | 'urgent';

// 任务状态
export type TaskStatus = 'todo' | 'doing' | 'done' | 'archived';

// 标签
export interface Tag {
  id: string;
  name: string;
  color: string;
  createdAt: string;
}

// 评论
export interface Comment {
  id: string;
  taskId: string;
  userId: string;
  content: string;
  mentions: string[];
  createdAt: string;
  updatedAt: string;
}

// 附件
export interface Attachment {
  id: string;
  taskId: string;
  filename: string;
  url: string;
  type: 'image' | 'document' | 'other';
  size: number;
  createdAt: string;
}

// 任务
export interface Task {
  id: string;
  title: string;
  description?: string;
  columnId: string;
  boardId: string;
  priority: TaskPriority;
  tags: string[];
  dueDate?: string;
  assigneeId?: string;
  createdAt: string;
  updatedAt: string;
  comments?: Comment[];
  attachments?: Attachment[];
}

// 看板列
export interface Column {
  id: string;
  name: string;
  boardId: string;
  order: number;
  tasks: Task[];
  createdAt: string;
  updatedAt: string;
}

// 看板
export interface Board {
  id: string;
  name: string;
  description?: string;
  ownerId: string;
  isPublic: boolean;
  columns: Column[];
  members: string[];
  createdAt: string;
  updatedAt: string;
}

// 用户
export interface User {
  id: string;
  username: string;
  email: string;
  avatar?: string;
  telegramId?: string;
  createdAt: string;
}

// API响应
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// 同步数据
export interface SyncData {
  boards: Board[];
  tasks: Task[];
  tags: Tag[];
  lastSync: string;
}

// 搜索参数
export interface SearchParams {
  query?: string;
  tags?: string[];
  status?: TaskStatus[];
  priority?: TaskPriority[];
  fromDate?: string;
  toDate?: string;
  assigneeId?: string;
  boardId?: string;
}