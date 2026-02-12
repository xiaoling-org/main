/**
 * 任务详情页面
 */

import React, {useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import {
  Appbar,
  Card,
  TextInput,
  Button,
  Chip,
  Divider,
  Avatar,
  FAB,
} from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import {useNavigation, useRoute} from '@react-navigation/native';
import {useStore} from '@/store';
import {Task, Comment} from '@/types';
import dayjs from 'dayjs';

const TaskScreen: React.FC = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const store = useStore();
  const {boards, updateTask} = store();

  const taskId = (route.params as any)?.taskId;
  const [editing, setEditing] = useState(false);
  const [newComment, setNewComment] = useState('');
  const [taskUpdates, setTaskUpdates] = useState<Partial<Task>>({});

  // 查找任务
  let task: Task | null = null;
  let boardId = '';
  let columnId = '';

  for (const board of boards) {
    for (const column of board.columns) {
      const foundTask = column.tasks.find(t => t.id === taskId);
      if (foundTask) {
        task = foundTask;
        boardId = board.id;
        columnId = column.id;
        break;
      }
    }
    if (task) break;
  }

  if (!task) {
    return (
      <SafeAreaView style={styles.container}>
        <Appbar.Header>
          <Appbar.BackAction onPress={() => navigation.goBack()} />
          <Appbar.Content title="任务未找到" />
        </Appbar.Header>
        <View style={styles.notFound}>
          <Icon name="alert-circle" size={64} color="#ccc" />
          <Text style={styles.notFoundText}>任务不存在或已被删除</Text>
          <Button mode="contained" onPress={() => navigation.goBack()}>
            返回
          </Button>
        </View>
      </SafeAreaView>
    );
  }

  // 合并更新
  const currentTask = {...task, ...taskUpdates};

  // 优先级选项
  const priorityOptions = [
    {id: 'low', label: '低', color: '#4CAF50', icon: 'arrow-down'},
    {id: 'medium', label: '中', color: '#FF9800', icon: 'arrow-right'},
    {id: 'high', label: '高', color: '#F44336', icon: 'arrow-up'},
    {id: 'urgent', label: '紧急', color: '#9C27B0', icon: 'alert'},
  ];

  // 状态选项
  const statusOptions = [
    {id: 'todo', label: '待处理', color: '#FFEBEE'},
    {id: 'doing', label: '进行中', color: '#FFF3E0'},
    {id: 'done', label: '已完成', color: '#E8F5E9'},
  ];

  // 标签选项
  const tagOptions = [
    {id: 'design', label: '设计', color: '#2196F3'},
    {id: 'development', label: '开发', color: '#4CAF50'},
    {id: 'bug', label: 'Bug', color: '#F44336'},
    {id: 'feature', label: '功能', color: '#9C27B0'},
    {id: 'documentation', label: '文档', color: '#FF9800'},
    {id: 'urgent', label: '紧急', color: '#FF4444'},
  ];

  // 处理更新
  const handleUpdate = (updates: Partial<Task>) => {
    setTaskUpdates({...taskUpdates, ...updates});
  };

  // 保存更改
  const handleSave = () => {
    if (Object.keys(taskUpdates).length > 0) {
      updateTask(taskId, taskUpdates);
      setTaskUpdates({});
    }
    setEditing(false);
  };

  // 添加评论
  const handleAddComment = () => {
    if (!newComment.trim()) return;

    const comment: Comment = {
      id: Date.now().toString(),
      taskId,
      userId: 'current-user',
      content: newComment,
      mentions: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    const updatedComments = [...(currentTask.comments || []), comment];
    handleUpdate({comments: updatedComments});
    setNewComment('');
  };

  // 渲染评论
  const renderComment = (comment: Comment, index: number) => (
    <View key={comment.id} style={styles.comment}>
      <Avatar.Text size={32} label="U" style={styles.commentAvatar} />
      <View style={styles.commentContent}>
        <View style={styles.commentHeader}>
          <Text style={styles.commentUser}>{comment.userId}</Text>
          <Text style={styles.commentTime}>
            {dayjs(comment.createdAt).fromNow()}
          </Text>
        </View>
        <Text style={styles.commentText}>{comment.content}</Text>
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <Appbar.Header>
        <Appbar.BackAction onPress={() => navigation.goBack()} />
        <Appbar.Content
          title={editing ? '编辑任务' : '任务详情'}
          subtitle={`#${taskId.slice(-6)}`}
        />
        <Appbar.Action
          icon={editing ? 'check' : 'pencil'}
          onPress={() => (editing ? handleSave() : setEditing(true))}
        />
        <Appbar.Action icon="dots-vertical" onPress={() => {}} />
      </Appbar.Header>

      <ScrollView style={styles.content}>
        {/* 任务标题 */}
        <Card style={styles.sectionCard}>
          <Card.Content>
            {editing ? (
              <TextInput
                label="任务标题"
                value={taskUpdates.title || currentTask.title}
                onChangeText={text => handleUpdate({title: text})}
                mode="outlined"
                style={styles.titleInput}
              />
            ) : (
              <Text style={styles.taskTitle}>{currentTask.title}</Text>
            )}
          </Card.Content>
        </Card>

        {/* 任务状态和优先级 */}
        <Card style={styles.sectionCard}>
          <Card.Content>
            <View style={styles.quickActions}>
              {/* 状态选择 */}
              <View style={styles.actionGroup}>
                <Text style={styles.actionLabel}>状态</Text>
                <View style={styles.chipGroup}>
                  {statusOptions.map(status => (
                    <Chip
                      key={status.id}
                      selected={currentTask.columnId === status.id}
                      onPress={() => handleUpdate({columnId: status.id})}
                      style={[
                        styles.statusChip,
                        {backgroundColor: status.color},
                      ]}
                      textStyle={styles.chipText}>
                      {status.label}
                    </Chip>
                  ))}
                </View>
              </View>

              {/* 优先级选择 */}
              <View style={styles.actionGroup}>
                <Text style={styles.actionLabel}>优先级</Text>
                <View style={styles.chipGroup}>
                  {priorityOptions.map(priority => (
                    <Chip
                      key={priority.id}
                      selected={currentTask.priority === priority.id}
                      onPress={() => handleUpdate({priority: priority.id as any})}
                      style={styles.priorityChip}
                      textStyle={[
                        styles.chipText,
                        {color: priority.color},
                      ]}>
                      <Icon name={priority.icon} size={16} color={priority.color} />
                      <Text style={{color: priority.color, marginLeft: 4}}>
                        {priority.label}
                      </Text>
                    </Chip>
                  ))}
                </View>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* 任务描述 */}
        <Card style={styles.sectionCard}>
          <Card.Content>
            <View style={styles.sectionHeader}>
              <Icon name="text" size={20} color="#666" />
              <Text style={styles.sectionTitle}>描述</Text>
            </View>
            {editing ? (
              <TextInput
                label="任务描述"
                value={taskUpdates.description || currentTask.description || ''}
                onChangeText={text => handleUpdate({description: text})}
                mode="outlined"
                multiline
                numberOfLines={4}
                style={styles.descriptionInput}
              />
            ) : (
              <Text style={styles.description}>
                {currentTask.description || '暂无描述'}
              </Text>
            )}
          </Card.Content>
        </Card>

        {/* 标签 */}
        <Card style={styles.sectionCard}>
          <Card.Content>
            <View style={styles.sectionHeader}>
              <Icon name="tag" size={20} color="#666" />
              <Text style={styles.sectionTitle}>标签</Text>
            </View>
            <View style={styles.tagsContainer}>
              {tagOptions.map(tag => {
                const isSelected = currentTask.tags?.includes(tag.id);
                return (
                  <Chip
                    key={tag.id}
                    selected={isSelected}
                    onPress={() => {
                      const currentTags = currentTask.tags || [];
                      const newTags = isSelected
                        ? currentTags.filter(t => t !== tag.id)
                        : [...currentTags, tag.id];
                      handleUpdate({tags: newTags});
                    }}
                    style={[
                      styles.tagChip,
                      isSelected && {backgroundColor: tag.color},
                    ]}
                    textStyle={[
                      styles.tagText,
                      isSelected && {color: '#fff'},
                    ]}>
                    #{tag.label}
                  </Chip>
                );
              })}
            </View>
          </Card.Content>
        </Card>

        {/* 截止日期 */}
        <Card style={styles.sectionCard}>
          <Card.Content>
            <View style={styles.sectionHeader}>
              <Icon name="calendar" size={20} color="#666" />
              <Text style={styles.sectionTitle}>截止日期</Text>
            </View>
            {editing ? (
              <Button
                mode="outlined"
                icon="calendar"
                onPress={() => {
                  // 日期选择器
                }}>
                {currentTask.dueDate
                  ? dayjs(currentTask.dueDate).format('YYYY-MM-DD')
                  : '设置截止日期'}
              </Button>
            ) : (
              <View style={styles.dueDateInfo}>
                <Icon name="calendar" size={20} color="#666" />
                <Text style={styles.dueDateText}>
                  {currentTask.dueDate
                    ? dayjs(currentTask.dueDate).format('YYYY年MM月DD日')
                    : '未设置截止日期'}
                </Text>
              </View>
            )}
          </Card.Content>
        </Card>

        {/* 元信息 */}
        <Card style={styles.sectionCard}>
          <Card.Content>
            <View style={styles.metaInfo}>
              <View style={styles.metaItem}>
                <Icon name="clock-outline" size={16} color="#666" />
                <Text style={styles.metaText}>
                  创建: {dayjs(currentTask.createdAt).format('YYYY-MM-DD HH:mm')}
                </Text>
              </View>
              <View style={styles.metaItem}>
                <Icon name="update" size={16} color="#666" />
                <Text style={styles.metaText}>
                  更新: {dayjs(currentTask.updatedAt).format('YYYY-MM-DD HH:mm')}
                </Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* 评论区域 */}
        <Card style={styles.sectionCard}>
          <Card.Content>
            <View style={styles.sectionHeader}>
              <Icon name="comment" size={20} color="#666" />
              <Text style={styles.sectionTitle}>
                评论 ({currentTask.comments?.length || 0})
              </Text>
            </View>

            {/* 评论列表 */}
            {currentTask.comments && currentTask.comments.length > 0 ? (
              <View style={styles.commentsList}>
                {currentTask.comments.map(renderComment)}
              </View>
            ) : (
              <Text style={styles.noComments}>暂无评论</Text>
            )}

            <Divider style={styles.divider} />

            {/* 添加评论 */}
            <View style={styles.addComment}>
              <TextInput
                label="添加评论"
                value={newComment}
                onChangeText={setNewComment}
                mode="outlined"
                multiline
                style={styles.commentInput}
                right={
                  <TextInput.Icon
                    icon="send"
                    onPress={handleAddComment}
                    disabled={!newComment.trim()}
                  />
                }
              />
            </View>
          </Card.Content>
        </Card>
      </ScrollView>

      {/* 附件FAB */}
      <FAB
        style={styles.attachmentFab}
        icon="paperclip"
        onPress={() => {
          // 添加附件
        }}
        small
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  notFound: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32,
  },
  notFoundText: {
    fontSize: 18,
    color: '#666',
    marginVertical: 16,
  },
  content: {
    flex: 1,
    padding: 16,
  },
  sectionCard: {
    marginBottom: 16,
    elevation: 2,
  },
  taskTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    lineHeight: 32,
  },
  titleInput: {
    marginBottom: 8,
  },
  quickActions: {
    gap: 16,
  },
  actionGroup: {
    gap: 8,
  },
  actionLabel: {
    fontSize: 14,
    fontWeight: '500',
    color: '#666',
    marginBottom: 4,
  },
  chipGroup: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  statusChip: {
    height: 32,
  },
  priorityChip: {
    height: 32,
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#E0E0E0',
  },
  chipText: {
    fontSize: 12,
    fontWeight: '500',
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginLeft: 8,
  },
  description: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  descriptionInput: {
    marginTop: 8,
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  tagChip: {
    height: 32,
    backgroundColor: '#F5F5F5',
  },
  tagText: {
    fontSize: 12,
    color: '#666',
  },
  dueDateInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  dueDateText: {
    fontSize: 14,
    color: '#666',
  },
  metaInfo: {
    gap: 8,
  },
  metaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  metaText: {
    fontSize: 12,
    color: '#666',
  },
  commentsList: {
    gap: 16,
    marginBottom: 16,
  },
  comment: {
    flexDirection: 'row',
    gap: 12,
  },
  commentAvatar: {
    backgroundColor: '#2196F3',
  },
  commentContent: {
    flex: 1,
  },
  commentHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  commentUser: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
  },
  commentTime: {
    fontSize: 12,
    color: '#999',
  },
  commentText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  noComments: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
    paddingVertical: 16,
  },
  divider: {
    marginVertical: 16,
  },
  addComment: {
    marginTop: 8,
  },
  commentInput: {
    backgroundColor: '#fff',
  },
  attachmentFab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: '#2196F3',
  },
});

export default TaskScreen;