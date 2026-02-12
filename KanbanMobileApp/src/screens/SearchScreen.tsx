/**
 * 搜索页面 - 高级搜索和过滤
 */

import React, {useState, useEffect} from 'react';
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
  Searchbar,
  Card,
  Chip,
  Button,
  Divider,
  List,
  Checkbox,
} from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import {useNavigation} from '@react-navigation/native';
import {useStore} from '@/store';
import {Task, Tag} from '@/types';
import dayjs from 'dayjs';

const SearchScreen: React.FC = () => {
  const navigation = useNavigation();
  const store = useStore();
  const {boards, tags} = store();

  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Task[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [selectedStatus, setSelectedStatus] = useState<string[]>([]);
  const [selectedPriority, setSelectedPriority] = useState<string[]>([]);
  const [showFilters, setShowFilters] = useState(false);
  const [dateRange, setDateRange] = useState<'today' | 'week' | 'month' | 'all'>('all');

  // 从所有看板中提取任务
  const allTasks: Task[] = [];
  boards.forEach(board => {
    board.columns.forEach(column => {
      column.tasks.forEach(task => {
        allTasks.push({
          ...task,
          boardId: board.id,
          columnId: column.id,
        });
      });
    });
  });

  // 搜索函数
  const performSearch = () => {
    let results = allTasks;

    // 关键词搜索
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      results = results.filter(task =>
        task.title.toLowerCase().includes(query) ||
        (task.description && task.description.toLowerCase().includes(query))
      );
    }

    // 标签过滤
    if (selectedTags.length > 0) {
      results = results.filter(task =>
        selectedTags.some(tag => task.tags?.includes(tag))
      );
    }

    // 状态过滤
    if (selectedStatus.length > 0) {
      results = results.filter(task =>
        selectedStatus.includes(task.columnId)
      );
    }

    // 优先级过滤
    if (selectedPriority.length > 0) {
      results = results.filter(task =>
        selectedPriority.includes(task.priority)
      );
    }

    // 日期范围过滤
    if (dateRange !== 'all') {
      const now = dayjs();
      let startDate: dayjs.Dayjs;

      switch (dateRange) {
        case 'today':
          startDate = now.startOf('day');
          break;
        case 'week':
          startDate = now.subtract(7, 'day');
          break;
        case 'month':
          startDate = now.subtract(30, 'day');
          break;
        default:
          startDate = now.subtract(365, 'day');
      }

      results = results.filter(task =>
        dayjs(task.createdAt).isAfter(startDate)
      );
    }

    setSearchResults(results);
  };

  // 当搜索条件变化时执行搜索
  useEffect(() => {
    performSearch();
  }, [searchQuery, selectedTags, selectedStatus, selectedPriority, dateRange]);

  // 状态选项
  const statusOptions = [
    {id: 'todo', label: '待处理', color: '#FFEBEE'},
    {id: 'doing', label: '进行中', color: '#FFF3E0'},
    {id: 'done', label: '已完成', color: '#E8F5E9'},
  ];

  // 优先级选项
  const priorityOptions = [
    {id: 'low', label: '低', color: '#4CAF50', icon: 'arrow-down'},
    {id: 'medium', label: '中', color: '#FF9800', icon: 'arrow-right'},
    {id: 'high', label: '高', color: '#F44336', icon: 'arrow-up'},
    {id: 'urgent', label: '紧急', color: '#9C27B0', icon: 'alert'},
  ];

  // 日期范围选项
  const dateOptions = [
    {id: 'today', label: '今天'},
    {id: 'week', label: '本周'},
    {id: 'month', label: '本月'},
    {id: 'all', label: '全部'},
  ];

  // 渲染任务卡片
  const renderTaskCard = (task: Task) => {
    const board = boards.find(b => b.id === task.boardId);
    const column = board?.columns.find(c => c.id === task.columnId);
    const priority = priorityOptions.find(p => p.id === task.priority);

    return (
      <Card
        key={task.id}
        style={styles.resultCard}
        onPress={() => navigation.navigate('Task', {taskId: task.id} as never)}>
        <Card.Content>
          <View style={styles.taskHeader}>
            <Text style={styles.taskTitle} numberOfLines={2}>
              {task.title}
            </Text>
            {priority && (
              <View style={styles.priorityBadge}>
                <Icon
                  name={priority.icon}
                  size={12}
                  color={priority.color}
                />
              </View>
            )}
          </View>

          <View style={styles.taskMeta}>
            <View style={styles.metaItem}>
              <Icon name="view-column" size={12} color="#666" />
              <Text style={styles.metaText}>
                {board?.name} • {column?.name}
              </Text>
            </View>
            <Text style={styles.taskDate}>
              {dayjs(task.createdAt).format('MM/DD')}
            </Text>
          </View>

          {task.tags && task.tags.length > 0 && (
            <View style={styles.tagsContainer}>
              {task.tags.slice(0, 3).map((tagId, index) => {
                const tag = tags.find(t => t.id === tagId);
                return (
                  <View
                    key={index}
                    style={[styles.tag, {backgroundColor: tag?.color || '#E0E0E0'}]}>
                    <Text style={styles.tagText}>
                      #{tag?.name || tagId}
                    </Text>
                  </View>
                );
              })}
              {task.tags.length > 3 && (
                <Text style={styles.moreTags}>+{task.tags.length - 3}</Text>
              )}
            </View>
          )}

          {task.description && (
            <Text style={styles.taskDescription} numberOfLines={2}>
              {task.description}
            </Text>
          )}
        </Card.Content>
      </Card>
    );
  };

  // 渲染过滤器面板
  const renderFilters = () => (
    <Card style={styles.filtersCard}>
      <Card.Content>
        {/* 日期范围 */}
        <View style={styles.filterSection}>
          <Text style={styles.filterTitle}>时间范围</Text>
          <View style={styles.chipGroup}>
            {dateOptions.map(option => (
              <Chip
                key={option.id}
                selected={dateRange === option.id}
                onPress={() => setDateRange(option.id as any)}
                style={styles.dateChip}>
                {option.label}
              </Chip>
            ))}
          </View>
        </View>

        <Divider style={styles.divider} />

        {/* 状态过滤 */}
        <View style={styles.filterSection}>
          <Text style={styles.filterTitle}>状态</Text>
          <View style={styles.checkboxGroup}>
            {statusOptions.map(status => (
              <TouchableOpacity
                key={status.id}
                style={styles.checkboxItem}
                onPress={() => {
                  const newStatus = selectedStatus.includes(status.id)
                    ? selectedStatus.filter(s => s !== status.id)
                    : [...selectedStatus, status.id];
                  setSelectedStatus(newStatus);
                }}>
                <Checkbox.Android
                  status={selectedStatus.includes(status.id) ? 'checked' : 'unchecked'}
                  color={status.color}
                />
                <Text style={styles.checkboxLabel}>{status.label}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <Divider style={styles.divider} />

        {/* 优先级过滤 */}
        <View style={styles.filterSection}>
          <Text style={styles.filterTitle}>优先级</Text>
          <View style={styles.checkboxGroup}>
            {priorityOptions.map(priority => (
              <TouchableOpacity
                key={priority.id}
                style={styles.checkboxItem}
                onPress={() => {
                  const newPriority = selectedPriority.includes(priority.id)
                    ? selectedPriority.filter(p => p !== priority.id)
                    : [...selectedPriority, priority.id];
                  setSelectedPriority(newPriority);
                }}>
                <Checkbox.Android
                  status={selectedPriority.includes(priority.id) ? 'checked' : 'unchecked'}
                  color={priority.color}
                />
                <View style={styles.priorityOption}>
                  <Icon
                    name={priority.icon}
                    size={16}
                    color={priority.color}
                  />
                  <Text style={[styles.checkboxLabel, {color: priority.color}]}>
                    {priority.label}
                  </Text>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <Divider style={styles.divider} />

        {/* 标签过滤 */}
        <View style={styles.filterSection}>
          <Text style={styles.filterTitle}>标签</Text>
          <View style={styles.tagsFilter}>
            {tags.slice(0, 10).map(tag => (
              <Chip
                key={tag.id}
                selected={selectedTags.includes(tag.id)}
                onPress={() => {
                  const newTags = selectedTags.includes(tag.id)
                    ? selectedTags.filter(t => t !== tag.id)
                    : [...selectedTags, tag.id];
                  setSelectedTags(newTags);
                }}
                style={[
                  styles.tagChip,
                  selectedTags.includes(tag.id) && {backgroundColor: tag.color},
                ]}
                textStyle={[
                  styles.tagChipText,
                  selectedTags.includes(tag.id) && {color: '#fff'},
                ]}>
                #{tag.name}
              </Chip>
            ))}
          </View>
          {tags.length > 10 && (
            <Text style={styles.moreTagsHint}>
              还有 {tags.length - 10} 个标签...
            </Text>
          )}
        </View>

        {/* 清除过滤器 */}
        {(selectedTags.length > 0 || selectedStatus.length > 0 || selectedPriority.length > 0) && (
          <Button
            mode="outlined"
            style={styles.clearButton}
            onPress={() => {
              setSelectedTags([]);
              setSelectedStatus([]);
              setSelectedPriority([]);
              setDateRange('all');
            }}>
            清除所有过滤器
          </Button>
        )}
      </Card.Content>
    </Card>
  );

  return (
    <SafeAreaView style={styles.container}>
      <Appbar.Header>
        <Appbar.BackAction onPress={() => navigation.goBack()} />
        <Appbar.Content title="搜索" />
        <Appbar.Action
          icon="filter"
          onPress={() => setShowFilters(!showFilters)}
        />
      </Appbar.Header>

      <View style={styles.searchContainer}>
        <Searchbar
          placeholder="搜索任务标题或描述..."
          value={searchQuery}
          onChangeText={setSearchQuery}
          style={styles.searchBar}
          iconColor="#666"
        />
      </View>

      <ScrollView style={styles.content}>
        {/* 过滤器面板 */}
        {showFilters && renderFilters()}

        {/* 搜索结果统计 */}
        <View style={styles.resultsHeader}>
          <Text style={styles.resultsTitle}>
            搜索结果 ({searchResults.length})
          </Text>
          {searchQuery && (
            <Text style={styles.searchQuery}>
              关键词: "{searchQuery}"
            </Text>
          )}
        </View>

        {/* 搜索结果 */}
        {searchResults.length > 0 ? (
          <View style={styles.resultsList}>
            {searchResults.map(renderTaskCard)}
          </View>
        ) : (
          <Card style={styles.noResultsCard}>
            <Card.Content style={styles.noResultsContent}>
              <Icon name="magnify" size={64} color="#ccc" />
              <Text style={styles.noResultsText}>
                {searchQuery || selectedTags.length > 0 || selectedStatus.length > 0 || selectedPriority.length > 0
                  ? '没有找到匹配的任务'
                  : '输入关键词或选择过滤器开始搜索'}
              </Text>
              {allTasks.length > 0 && (
                <Text style={styles.totalTasksHint}>
                  共有 {allTasks.length} 个任务可搜索
                </Text>
              )}
            </Card.Content>
          </Card>
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  searchContainer: {
    padding: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  searchBar: {
    elevation: 0,
    backgroundColor: '#F5F5F5',
  },
  content: {
    flex: 1,
    padding: 16,
  },
  filtersCard: {
    marginBottom: 16,
    elevation: 2,
  },
  filterSection: {
    marginBottom: 16,
  },
  filterTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
  },
  chipGroup: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  dateChip: {
    height: 32,
  },
  checkboxGroup: {
    gap: 12,
  },
  checkboxItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  checkboxLabel: {
    fontSize: 14,
    color: '#333',
    marginLeft: 8,
  },
  priorityOption: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  tagsFilter: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  tagChip: {
    height: 32,
    backgroundColor: '#F5F5F5',
  },
  tagChipText: {
    fontSize: 12,
    color: '#666',
  },
  moreTagsHint: {
    fontSize: 12,
    color: '#999',
    marginTop: 8,
    fontStyle: 'italic',
  },
  divider: {
    marginVertical: 16,
  },
  clearButton: {
    marginTop: 8,
  },
  resultsHeader: {
    marginBottom: 16,
  },
  resultsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  searchQuery: {
    fontSize: 14,
    color: '#666',
    fontStyle: 'italic',
  },
  resultsList: {
    gap: 12,
  },
  resultCard: {
    elevation: 1,
  },
  taskHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  taskTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
    flex: 1,
    marginRight: 8,
  },
  priorityBadge: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: '#F5F5F5',
    justifyContent: 'center',
    alignItems: 'center',
  },
  taskMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  metaItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  metaText: {
    fontSize: 12,
    color: '#666',
    marginLeft: 4,
  },
  taskDate: {
    fontSize: 12,
    color: '#999',
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 8,
  },
  tag: {
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
    marginRight: 4,
    marginBottom: 4,
  },
  tagText: {
    fontSize: 10,
    color: '#fff',
    fontWeight: '500',
  },
  moreTags: {
    fontSize: 10,
    color: '#666',
    alignSelf: 'center',
    marginLeft: 4,
  },
  taskDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 18,
  },
  noResultsCard: {
    elevation: 2,
  },
  noResultsContent: {
    alignItems: 'center',
    paddingVertical: 48,
  },
  noResultsText: {
    fontSize: 16,
    color: '#999',
    textAlign: 'center',
    marginVertical: 16,
  },
  totalTasksHint: {
    fontSize: 14,
    color: '#666',
    marginTop: 8,
  },
});

export default SearchScreen;