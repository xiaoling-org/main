/**
 * WebSocket实时通信服务
 * 用于看板系统的实时更新
 */

import { io } from 'socket.io-client';
import { Platform } from 'react-native';

class WebSocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.listeners = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    
    // 根据平台选择服务器地址
    this.serverUrl = Platform.select({
      ios: 'http://localhost:5000',
      android: 'http://10.0.2.2:5000',
      web: 'http://localhost:5000',
      default: 'http://localhost:5000'
    });
  }

  /**
   * 连接到WebSocket服务器
   */
  connect(userId) {
    if (this.socket && this.isConnected) {
      console.log('WebSocket already connected');
      return;
    }

    try {
      this.socket = io(this.serverUrl, {
        transports: ['websocket', 'polling'],
        reconnection: true,
        reconnectionAttempts: this.maxReconnectAttempts,
        reconnectionDelay: this.reconnectDelay,
        timeout: 10000
      });

      // 连接成功
      this.socket.on('connect', () => {
        console.log('✅ WebSocket connected:', this.socket.id);
        this.isConnected = true;
        this.reconnectAttempts = 0;
        
        // 通知所有连接监听器
        this.emitToListeners('connected', { socketId: this.socket.id });
        
        // 自动加入默认看板
        if (userId) {
          this.joinBoard('default', userId);
        }
      });

      // 连接错误
      this.socket.on('connect_error', (error) => {
        console.error('❌ WebSocket connection error:', error);
        this.isConnected = false;
        this.emitToListeners('connection_error', error);
      });

      // 断开连接
      this.socket.on('disconnect', (reason) => {
        console.log('📡 WebSocket disconnected:', reason);
        this.isConnected = false;
        this.emitToListeners('disconnected', { reason });
        
        // 自动重连
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          setTimeout(() => {
            console.log(`🔄 Reconnecting (attempt ${this.reconnectAttempts})...`);
            this.socket.connect();
          }, this.reconnectDelay * this.reconnectAttempts);
        }
      });

      // 服务器事件
      this.setupEventListeners();

    } catch (error) {
      console.error('❌ WebSocket initialization error:', error);
    }
  }

  /**
   * 设置事件监听器
   */
  setupEventListeners() {
    // 任务更新事件
    this.socket.on('task_update', (data) => {
      console.log('🔄 Task update received:', data);
      this.emitToListeners('task_update', data);
    });

    // 任务移动事件
    this.socket.on('task_move', (data) => {
      console.log('🔄 Task move received:', data);
      this.emitToListeners('task_move', data);
    });

    // 评论添加事件
    this.socket.on('comment_add', (data) => {
      console.log('💬 Comment received:', data);
      this.emitToListeners('comment_add', data);
    });

    // 用户输入指示器
    this.socket.on('user_typing_indicator', (data) => {
      this.emitToListeners('user_typing', data);
    });

    // 在线用户列表
    this.socket.on('online_users', (data) => {
      this.emitToListeners('online_users', data);
    });

    // 连接确认
    this.socket.on('connected', (data) => {
      this.emitToListeners('socket_connected', data);
    });

    // 看板加入确认
    this.socket.on('board_joined', (data) => {
      this.emitToListeners('board_joined', data);
    });
  }

  /**
   * 加入看板房间
   */
  joinBoard(boardId, userId) {
    if (!this.isConnected || !this.socket) {
      console.warn('Cannot join board: WebSocket not connected');
      return;
    }

    this.socket.emit('join_board', {
      board_id: boardId,
      user_id: userId
    });
    
    console.log(`👥 Joining board: ${boardId} as user: ${userId}`);
  }

  /**
   * 离开看板房间
   */
  leaveBoard(boardId) {
    if (!this.isConnected || !this.socket) {
      return;
    }

    this.socket.emit('leave_board', {
      board_id: boardId
    });
  }

  /**
   * 发送任务更新
   */
  sendTaskUpdate(action, taskId, data, userId) {
    if (!this.isConnected || !this.socket) {
      return;
    }

    this.socket.emit('task_updated', {
      board_id: 'default',
      task_id: taskId,
      action: action,
      user_id: userId,
      data: data,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 发送任务移动
   */
  sendTaskMove(taskId, fromColumn, toColumn, userId) {
    if (!this.isConnected || !this.socket) {
      return;
    }

    this.socket.emit('task_moved', {
      board_id: 'default',
      task_id: taskId,
      from_column: fromColumn,
      to_column: toColumn,
      user_id: userId
    });
  }

  /**
   * 发送评论
   */
  sendComment(taskId, commentId, content, userId) {
    if (!this.isConnected || !this.socket) {
      return;
    }

    this.socket.emit('comment_added', {
      board_id: 'default',
      task_id: taskId,
      comment_id: commentId,
      user_id: userId,
      content: content
    });
  }

  /**
   * 发送用户正在输入指示
   */
  sendTypingIndicator(taskId, userId) {
    if (!this.isConnected || !this.socket) {
      return;
    }

    this.socket.emit('user_typing', {
      board_id: 'default',
      task_id: taskId,
      user_id: userId
    });
  }

  /**
   * 获取在线用户
   */
  getOnlineUsers() {
    if (!this.isConnected || !this.socket) {
      return;
    }

    this.socket.emit('get_online_users', {
      board_id: 'default'
    });
  }

  /**
   * 断开连接
   */
  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.isConnected = false;
      this.listeners.clear();
      console.log('👋 WebSocket disconnected manually');
    }
  }

  /**
   * 添加事件监听器
   */
  addListener(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
    
    // 返回移除函数
    return () => {
      const callbacks = this.listeners.get(event);
      if (callbacks) {
        const index = callbacks.indexOf(callback);
        if (index > -1) {
          callbacks.splice(index, 1);
        }
      }
    };
  }

  /**
   * 触发监听器事件
   */
  emitToListeners(event, data) {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in ${event} listener:`, error);
        }
      });
    }
  }

  /**
   * 获取连接状态
   */
  getConnectionStatus() {
    return {
      isConnected: this.isConnected,
      socketId: this.socket?.id,
      serverUrl: this.serverUrl,
      reconnectAttempts: this.reconnectAttempts
    };
  }
}

// 创建单例实例
const webSocketService = new WebSocketService();

export default webSocketService;