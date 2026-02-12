/**
 * 首页屏幕
 */

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  SafeAreaView,
} from 'react-native';
import {Card, Button, Avatar, FAB} from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import {useNavigation} from '@react-navigation/native';
import {useStore} from '@/store';

const HomeScreen: React.FC = () => {
  const navigation = useNavigation();
  const store = useStore();
  const {boards, user} = store();

  // 示例数据
  const recentBoards = boards.slice(0, 3);
  const quickActions = [
    {id: 1, title: '添加任务', icon: 'plus', color: '#2196F3'},
    {id: 2, title: '快速搜索', icon: 'magnify', color: '#4CAF50'},
    {id: 3, title: '今日任务', icon: 'calendar-today', color: '#FF9800'},
    {id: 4, title: '团队协作', icon: 'account-group', color: '#9C27B0'},
  ];

  const stats = {
    totalTasks: 24,
    completed: 8,
    inProgress: 6,
    overdue: 2,
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        {/* 头部欢迎区域 */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>
              {user ? `你好，${user.username}` : '你好，用户'}
            </Text>
            <Text style={styles.subtitle}>今天有什么计划？</Text>
          </View>
          <Avatar.Text size={40} label="XL" />
        </View>

        {/* 统计卡片 */}
        <Card style={styles.statsCard}>
          <Card.Content>
            <View style={styles.statsRow}>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{stats.totalTasks}</Text>
                <Text style={styles.statLabel}>总任务</Text>
              </View>
              <View style={styles.statDivider} />
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{stats.completed}</Text>
                <Text style={styles.statLabel}>已完成</Text>
              </View>
              <View style={styles.statDivider} />
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{stats.inProgress}</Text>
                <Text style={styles.statLabel}>进行中</Text>
              </View>
              <View style={styles.statDivider} />
              <View style={styles.statItem}>
                <Text style={[styles.statNumber, styles.overdue]}>
                  {stats.overdue}
                </Text>
                <Text style={styles.statLabel}>已逾期</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* 快速操作 */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>快速操作</Text>
          <View style={styles.quickActions}>
            {quickActions.map(action => (
              <TouchableOpacity
                key={action.id}
                style={styles.actionButton}
                onPress={() => {
                  if (action.id === 1) {
                    // 导航到添加任务
                  }
                }}>
                <View
                  style={[styles.actionIcon, {backgroundColor: action.color}]}>
                  <Icon name={action.icon} size={24} color="#fff" />
                </View>
                <Text style={styles.actionText}>{action.title}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* 最近看板 */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>最近看板</Text>
            <Button
              mode="text"
              onPress={() => navigation.navigate('Boards' as never)}>
              查看全部
            </Button>
          </View>

          {recentBoards.length > 0 ? (
            recentBoards.map(board => (
              <Card
                key={board.id}
                style={styles.boardCard}
                onPress={() =>
                  navigation.navigate('Board', {boardId: board.id} as never)
                }>
                <Card.Content>
                  <View style={styles.boardHeader}>
                    <Icon name="view-column" size={20} color="#666" />
                    <Text style={styles.boardTitle}>{board.name}</Text>
                  </View>
                  <Text style={styles.boardDescription} numberOfLines={2}>
                    {board.description || '暂无描述'}
                  </Text>
                  <View style={styles.boardFooter}>
                    <View style={styles.boardStats}>
                      <Icon name="checkbox-multiple-marked" size={16} color="#666" />
                      <Text style={styles.boardStatText}>
                        {board.columns.reduce(
                          (total, col) => total + col.tasks.length,
                          0,
                        )}{' '}
                        个任务
                      </Text>
                    </View>
                    <Text style={styles.boardUpdated}>
                      更新于 {new Date(board.updatedAt).toLocaleDateString()}
                    </Text>
                  </View>
                </Card.Content>
              </Card>
            ))
          ) : (
            <Card style={styles.emptyCard}>
              <Card.Content style={styles.emptyContent}>
                <Icon name="view-column-outline" size={48} color="#ccc" />
                <Text style={styles.emptyText}>暂无看板</Text>
                <Button
                  mode="contained"
                  onPress={() => {
                    // 创建新看板
                  }}>
                  创建第一个看板
                </Button>
              </Card.Content>
            </Card>
          )}
        </View>

        {/* 今日任务 */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>今日任务</Text>
            <Button mode="text">查看全部</Button>
          </View>

          <Card style={styles.todayCard}>
            <Card.Content>
              <View style={styles.todayTask}>
                <Icon name="checkbox-blank-circle-outline" size={24} color="#666" />
                <View style={styles.taskContent}>
                  <Text style={styles.taskTitle}>完成APP首页设计</Text>
                  <Text style={styles.taskInfo}>工作项目 · 今天 18:00</Text>
                </View>
                <View style={styles.taskTags}>
                  <View style={[styles.tag, {backgroundColor: '#FF4444'}]}>
                    <Text style={styles.tagText}>紧急</Text>
                  </View>
                </View>
              </View>

              <View style={styles.todayTask}>
                <Icon name="checkbox-blank-circle-outline" size={24} color="#666" />
                <View style={styles.taskContent}>
                  <Text style={styles.taskTitle}>编写API文档</Text>
                  <Text style={styles.taskInfo}>学习计划 · 今天 20:00</Text>
                </View>
                <View style={styles.taskTags}>
                  <View style={[styles.tag, {backgroundColor: '#FFAA00'}]}>
                    <Text style={styles.tagText}>重要</Text>
                  </View>
                </View>
              </View>
            </Card.Content>
          </Card>
        </View>
      </ScrollView>

      {/* 浮动操作按钮 */}
      <FAB
        style={styles.fab}
        icon="plus"
        onPress={() => {
          // 添加任务
        }}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#fff',
  },
  greeting: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  statsCard: {
    margin: 16,
    elevation: 2,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
  },
  statItem: {
    alignItems: 'center',
    flex: 1,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  overdue: {
    color: '#F44336',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  statDivider: {
    width: 1,
    height: 30,
    backgroundColor: '#E0E0E0',
  },
  section: {
    marginTop: 16,
    paddingHorizontal: 16,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  quickActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
  },
  actionButton: {
    alignItems: 'center',
    width: '23%',
    marginBottom: 12,
  },
  actionIcon: {
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  actionText: {
    fontSize: 12,
    color: '#333',
    textAlign: 'center',
  },
  boardCard: {
    marginBottom: 12,
    elevation: 2,
  },
  boardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  boardTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginLeft: 8,
  },
  boardDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
    lineHeight: 20,
  },
  boardFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  boardStats: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  boardStatText: {
    fontSize: 12,
    color: '#666',
    marginLeft: 4,
  },
  boardUpdated: {
    fontSize: 12,
    color: '#999',
  },
  emptyCard: {
    marginBottom: 12,
    elevation: 2,
  },
  emptyContent: {
    alignItems: 'center',
    paddingVertical: 32,
  },
  emptyText: {
    fontSize: 16,
    color: '#999',
    marginVertical: 16,
  },
  todayCard: {
    elevation: 2,
  },
  todayTask: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  taskContent: {
    flex: 1,
    marginLeft: 12,
  },
  taskTitle: {
    fontSize: 16,
    color: '#333',
    marginBottom: 4,
  },
  taskInfo: {
    fontSize: 12,
    color: '#666',
  },
  taskTags: {
    flexDirection: 'row',
  },
  tag: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
    marginLeft: 4,
  },
  tagText: {
    fontSize: 10,
    color: '#fff',
    fontWeight: '500',
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: '#2196F3',
  },
});

export default HomeScreen;