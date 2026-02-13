/**
 * 实时看板组件
 * 集成WebSocket实时更新功能
 */

import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, StyleSheet, Alert } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import webSocketService from '../services/websocket';
import apiService from '../services/api';

const RealTimeBoard = ({ boardId = 'default', userId, children }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [onlineUsers, setOnlineUsers] = useState([]);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');

  // 初始化WebSocket连接
  useEffect(() => {
    if (userId) {
      console.log('🔌 Initializing WebSocket for user:', userId);
      webSocketService.connect(userId);
    }

    // 添加连接状态监听器
    const removeConnectedListener = webSocketService.addListener('connected', (data) => {
      console.log('✅ WebSocket connected:', data);
      setIsConnected(true);
      setConnectionStatus('connected');
      
      // 加入看板
      webSocketService.joinBoard(boardId, userId);
      
      // 获取在线用户
      setTimeout(() => {
        webSocketService.getOnlineUsers();
      }, 1000);
    });

    const removeDisconnectedListener = webSocketService.addListener('disconnected', () => {
      console.log('📡 WebSocket disconnected');
      setIsConnected(false);
      setConnectionStatus('disconnected');
    });

    const removeConnectionErrorListener = webSocketService.addListener('connection_error', (error) => {
      console.error('❌ WebSocket connection error:', error);
      setConnectionStatus('error');
      
      // 显示错误提示（非阻塞）
      Alert.alert(
        '连接错误',
        '无法连接到实时服务器，将使用普通模式',
        [{ text: '确定' }]
      );
    });

    // 在线用户更新
    const removeOnlineUsersListener = webSocketService.addListener('online_users', (data) => {
      console.log('👥 Online users updated:', data.users.length);
      setOnlineUsers(data.users);
    });

    // 任务更新监听
    const removeTaskUpdateListener = webSocketService.addListener('task_update', (data) => {
      console.log('🔄 Real-time task update:', data);
      setLastUpdate(new Date().toISOString());
      
      // 通知父组件有更新（通过回调或Context）
      // 这里可以触发数据刷新
      if (data.user_id !== userId) { // 不是自己操作才提示
        Alert.alert(
          '任务更新',
          `用户 ${data.user_id} ${getActionText(data.action)} 了任务`,
          [{ text: '确定' }]
        );
      }
    });

    // 任务移动监听
    const removeTaskMoveListener = webSocketService.addListener('task_move', (data) => {
      console.log('🔄 Real-time task move:', data);
      setLastUpdate(new Date().toISOString());
      
      if (data.user_id !== userId) {
        // 更新本地任务位置
        // 这里可以集成到状态管理
      }
    });

    // 评论监听
    const removeCommentListener = webSocketService.addListener('comment_add', (data) => {
      console.log('💬 Real-time comment:', data);
      setLastUpdate(new Date().toISOString());
      
      if (data.user_id !== userId) {
        Alert.alert(
          '新评论',
          `用户 ${data.user_id} 在任务中添加了评论`,
          [{ text: '查看', onPress: () => navigateToTask(data.task_id) },
           { text: '忽略' }]
        );
      }
    });

    // 清理函数
    return () => {
      removeConnectedListener();
      removeDisconnectedListener();
      removeConnectionErrorListener();
      removeOnlineUsersListener();
      removeTaskUpdateListener();
      removeTaskMoveListener();
      removeCommentListener();
      
      // 离开看板
      webSocketService.leaveBoard(boardId);
    };
  }, [boardId, userId]);

  // 屏幕聚焦时重新连接
  useFocusEffect(
    useCallback(() => {
      if (userId && !isConnected) {
        console.log('🔄 Screen focused, reconnecting WebSocket...');
        webSocketService.connect(userId);
      }
      
      return () => {
        // 屏幕失焦时不 disconnect，保持后台连接
        console.log('📱 Screen unfocused, keeping WebSocket connection');
      };
    }, [userId, isConnected])
  );

  // 获取操作文本
  const getActionText = (action) => {
    const actions = {
      'created': '创建',
      'updated': '更新',
      'moved': '移动',
      'deleted': '删除'
    };
    return actions[action] || action;
  };

  // 导航到任务详情（占位函数）
  const navigateToTask = (taskId) => {
    console.log('Navigating to task:', taskId);
    // 实际实现中会调用导航
  };

  // 发送任务更新
  const sendTaskUpdate = (action, taskId, data) => {
    if (!isConnected) {
      console.warn('Cannot send update: WebSocket not connected');
      return false;
    }
    
    webSocketService.sendTaskUpdate(action, taskId, data, userId);
    return true;
  };

  // 发送任务移动
  const sendTaskMove = (taskId, fromColumn, toColumn) => {
    if (!isConnected) {
      console.warn('Cannot send move: WebSocket not connected');
      return false;
    }
    
    webSocketService.sendTaskMove(taskId, fromColumn, toColumn, userId);
    return true;
  };

  // 发送评论
  const sendComment = (taskId, commentId, content) => {
    if (!isConnected) {
      console.warn('Cannot send comment: WebSocket not connected');
      return false;
    }
    
    webSocketService.sendComment(taskId, commentId, content, userId);
    return true;
  };

  // 发送输入指示
  const sendTypingIndicator = (taskId) => {
    if (!isConnected) {
      return;
    }
    
    webSocketService.sendTypingIndicator(taskId, userId);
  };

  // 获取连接状态
  const getConnectionInfo = () => {
    return webSocketService.getConnectionStatus();
  };

  // 渲染连接状态指示器
  const renderConnectionStatus = () => {
    if (!userId) return null;

    const statusConfig = {
      connected: { color: '#4CAF50', text: '实时在线', icon: '●' },
      disconnected: { color: '#F44336', text: '离线模式', icon: '○' },
      connecting: { color: '#FF9800', text: '连接中...', icon: '⟳' },
      error: { color: '#9C27B0', text: '连接错误', icon: '⚠' }
    };

    const config = statusConfig[connectionStatus] || statusConfig.disconnected;

    return (
      <View style={[styles.statusBar, { backgroundColor: config.color + '20' }]}>
        <View style={[styles.statusDot, { backgroundColor: config.color }]} />
        <Text style={[styles.statusText, { color: config.color }]}>
          {config.text}
          {onlineUsers.length > 0 && ` · ${onlineUsers.length}人在线`}
        </Text>
        {lastUpdate && (
          <Text style={styles.lastUpdateText}>
            最后更新: {new Date(lastUpdate).toLocaleTimeString()}
          </Text>
        )}
      </View>
    );
  };

  return (
    <View style={styles.container}>
      {renderConnectionStatus()}
      
      {/* 渲染子组件，并传递实时功能 */}
      {React.Children.map(children, child => {
        if (React.isValidElement(child)) {
          return React.cloneElement(child, {
            // 传递实时功能给子组件
            isRealtimeConnected: isConnected,
            sendTaskUpdate,
            sendTaskMove,
            sendComment,
            sendTypingIndicator,
            onlineUsers,
            connectionInfo: getConnectionInfo()
          });
        }
        return child;
      })}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  statusBar: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 8,
  },
  statusText: {
    fontSize: 12,
    fontWeight: '500',
    flex: 1,
  },
  lastUpdateText: {
    fontSize: 10,
    color: '#757575',
    marginLeft: 8,
  },
});

export default RealTimeBoard;