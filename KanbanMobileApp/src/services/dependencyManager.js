/**
 * 任务依赖关系管理器
 * 管理任务之间的依赖关系，支持前置任务、后置任务、依赖检查等
 */

import AsyncStorage from '@react-native-async-storage/async-storage';

class DependencyManager {
  constructor() {
    this.dependencies = new Map(); // taskId -> {dependencies: [], dependents: []}
    this.initialized = false;
    this.STORAGE_KEY = '@kanban_dependencies';
  }

  /**
   * 初始化依赖管理器
   */
  async initialize() {
    if (this.initialized) return;

    try {
      const stored = await AsyncStorage.getItem(this.STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        // 恢复Map结构
        for (const [taskId, deps] of Object.entries(parsed)) {
          this.dependencies.set(taskId, deps);
        }
      }
      this.initialized = true;
      console.log('✅ Dependency manager initialized');
    } catch (error) {
      console.error('❌ Failed to initialize dependency manager:', error);
    }
  }

  /**
   * 保存依赖关系到存储
   */
  async saveToStorage() {
    try {
      const obj = Object.fromEntries(this.dependencies);
      await AsyncStorage.setItem(this.STORAGE_KEY, JSON.stringify(obj));
    } catch (error) {
      console.error('❌ Failed to save dependencies:', error);
    }
  }

  /**
   * 添加依赖关系
   * @param {string} taskId 任务ID
   * @param {string} dependsOnTaskId 依赖的任务ID
   */
  async addDependency(taskId, dependsOnTaskId) {
    await this.initialize();

    // 检查循环依赖
    if (this.wouldCreateCycle(taskId, dependsOnTaskId)) {
      throw new Error('添加此依赖将创建循环依赖');
    }

    // 更新依赖任务
    if (!this.dependencies.has(taskId)) {
      this.dependencies.set(taskId, { dependencies: [], dependents: [] });
    }
    const taskDeps = this.dependencies.get(taskId);
    if (!taskDeps.dependencies.includes(dependsOnTaskId)) {
      taskDeps.dependencies.push(dependsOnTaskId);
    }

    // 更新被依赖任务
    if (!this.dependencies.has(dependsOnTaskId)) {
      this.dependencies.set(dependsOnTaskId, { dependencies: [], dependents: [] });
    }
    const dependsOnTaskDeps = this.dependencies.get(dependsOnTaskId);
    if (!dependsOnTaskDeps.dependents.includes(taskId)) {
      dependsOnTaskDeps.dependents.push(taskId);
    }

    await this.saveToStorage();
    console.log(`🔗 Added dependency: ${taskId} -> ${dependsOnTaskId}`);
  }

  /**
   * 移除依赖关系
   */
  async removeDependency(taskId, dependsOnTaskId) {
    await this.initialize();

    if (this.dependencies.has(taskId)) {
      const taskDeps = this.dependencies.get(taskId);
      taskDeps.dependencies = taskDeps.dependencies.filter(id => id !== dependsOnTaskId);
    }

    if (this.dependencies.has(dependsOnTaskId)) {
      const dependsOnTaskDeps = this.dependencies.get(dependsOnTaskId);
      dependsOnTaskDeps.dependents = dependsOnTaskDeps.dependents.filter(id => id !== taskId);
    }

    await this.saveToStorage();
    console.log(`🔗 Removed dependency: ${taskId} -> ${dependsOnTaskId}`);
  }

  /**
   * 获取任务的所有依赖
   */
  async getDependencies(taskId) {
    await this.initialize();
    return this.dependencies.get(taskId)?.dependencies || [];
  }

  /**
   * 获取任务的所有依赖者
   */
  async getDependents(taskId) {
    await this.initialize();
    return this.dependencies.get(taskId)?.dependents || [];
  }

  /**
   * 获取任务的完整依赖链
   */
  async getDependencyChain(taskId) {
    await this.initialize();
    
    const chain = {
      ancestors: [], // 所有祖先任务（前置依赖）
      descendants: [] // 所有后代任务（后置依赖）
    };

    // 递归获取祖先
    const getAncestors = (currentId, visited = new Set()) => {
      if (visited.has(currentId)) return;
      visited.add(currentId);

      const deps = this.dependencies.get(currentId)?.dependencies || [];
      for (const depId of deps) {
        if (!chain.ancestors.includes(depId)) {
          chain.ancestors.push(depId);
        }
        getAncestors(depId, visited);
      }
    };

    // 递归获取后代
    const getDescendants = (currentId, visited = new Set()) => {
      if (visited.has(currentId)) return;
      visited.add(currentId);

      const dependents = this.dependencies.get(currentId)?.dependents || [];
      for (const depId of dependents) {
        if (!chain.descendants.includes(depId)) {
          chain.descendants.push(depId);
        }
        getDescendants(depId, visited);
      }
    };

    getAncestors(taskId);
    getDescendants(taskId);

    return chain;
  }

  /**
   * 检查是否创建循环依赖
   */
  wouldCreateCycle(startId, targetId) {
    if (startId === targetId) return true;

    // 深度优先搜索检查循环
    const visited = new Set();
    const stack = [targetId];

    while (stack.length > 0) {
      const current = stack.pop();
      
      if (current === startId) {
        return true; // 发现循环
      }

      if (!visited.has(current)) {
        visited.add(current);
        const deps = this.dependencies.get(current)?.dependencies || [];
        stack.push(...deps);
      }
    }

    return false;
  }

  /**
   * 检查任务是否可以移动（依赖是否满足）
   */
  async canMoveTask(taskId, targetColumnId, tasks) {
    await this.initialize();

    // 如果目标列是"已完成"，需要检查所有依赖是否已完成
    if (targetColumnId === 'done') {
      const dependencies = await this.getDependencies(taskId);
      
      for (const depId of dependencies) {
        const depTask = tasks.find(t => t.id === depId);
        if (!depTask) continue;
        
        // 如果依赖任务不在"已完成"列，则不能移动
        if (depTask.column !== 'done') {
          return {
            canMove: false,
            reason: `依赖任务 "${depTask.title}" 尚未完成`,
            blockingTask: depTask
          };
        }
      }
    }

    return { canMove: true };
  }

  /**
   * 获取任务的阻塞状态
   */
  async getTaskBlockStatus(taskId, tasks) {
    await this.initialize();

    const dependencies = await this.getDependencies(taskId);
    const blockingTasks = [];

    for (const depId of dependencies) {
      const depTask = tasks.find(t => t.id === depId);
      if (depTask && depTask.column !== 'done') {
        blockingTasks.push(depTask);
      }
    }

    return {
      isBlocked: blockingTasks.length > 0,
      blockingTasks,
      dependencyCount: dependencies.length
    };
  }

  /**
   * 可视化依赖关系图数据
   */
  async getDependencyGraph(tasks) {
    await this.initialize();

    const nodes = [];
    const edges = [];

    // 创建节点
    for (const task of tasks) {
      const blockStatus = await this.getTaskBlockStatus(task.id, tasks);
      
      nodes.push({
        id: task.id,
        label: task.title,
        column: task.column,
        priority: task.priority,
        isBlocked: blockStatus.isBlocked,
        blockingTasks: blockStatus.blockingTasks
      });
    }

    // 创建边
    for (const [taskId, deps] of this.dependencies.entries()) {
      const taskDeps = deps.dependencies || [];
      for (const depId of taskDeps) {
        edges.push({
          from: depId,
          to: taskId,
          type: 'dependency'
        });
      }
    }

    return { nodes, edges };
  }

  /**
   * 批量更新依赖关系
   */
  async batchUpdateDependencies(updates) {
    await this.initialize();

    for (const update of updates) {
      if (update.type === 'add') {
        await this.addDependency(update.taskId, update.dependsOnTaskId);
      } else if (update.type === 'remove') {
        await this.removeDependency(update.taskId, update.dependsOnTaskId);
      }
    }
  }

  /**
   * 清除任务的所有依赖关系
   */
  async clearTaskDependencies(taskId) {
    await this.initialize();

    const taskDeps = this.dependencies.get(taskId);
    if (!taskDeps) return;

    // 移除所有依赖
    for (const depId of taskDeps.dependencies) {
      const depTaskDeps = this.dependencies.get(depId);
      if (depTaskDeps) {
        depTaskDeps.dependents = depTaskDeps.dependents.filter(id => id !== taskId);
      }
    }

    // 移除所有依赖者
    for (const depId of taskDeps.dependents) {
      const depTaskDeps = this.dependencies.get(depId);
      if (depTaskDeps) {
        depTaskDeps.dependencies = depTaskDeps.dependencies.filter(id => id !== taskId);
      }
    }

    // 移除任务本身
    this.dependencies.delete(taskId);

    await this.saveToStorage();
  }

  /**
   * 导出依赖关系
   */
  async exportDependencies() {
    await this.initialize();
    
    const exportData = {
      version: '1.0',
      timestamp: new Date().toISOString(),
      dependencies: Array.from(this.dependencies.entries())
    };

    return exportData;
  }

  /**
   * 导入依赖关系
   */
  async importDependencies(data) {
    try {
      if (data.version !== '1.0') {
        throw new Error('不支持的版本格式');
      }

      this.dependencies.clear();
      for (const [taskId, deps] of data.dependencies) {
        this.dependencies.set(taskId, deps);
      }

      await this.saveToStorage();
      console.log('✅ Dependencies imported successfully');
      return true;
    } catch (error) {
      console.error('❌ Failed to import dependencies:', error);
      return false;
    }
  }

  /**
   * 获取统计信息
   */
  async getStats() {
    await this.initialize();

    let totalDependencies = 0;
    let maxDependencies = 0;
    let tasksWithDependencies = 0;

    for (const [taskId, deps] of this.dependencies.entries()) {
      const depCount = deps.dependencies.length;
      if (depCount > 0) {
        tasksWithDependencies++;
        totalDependencies += depCount;
        maxDependencies = Math.max(maxDependencies, depCount);
      }
    }

    return {
      totalTasks: this.dependencies.size,
      tasksWithDependencies,
      totalDependencies,
      maxDependencies,
      avgDependencies: tasksWithDependencies > 0 ? (totalDependencies / tasksWithDependencies).toFixed(2) : 0
    };
  }
}

// 创建单例实例
const dependencyManager = new DependencyManager();

export default dependencyManager;