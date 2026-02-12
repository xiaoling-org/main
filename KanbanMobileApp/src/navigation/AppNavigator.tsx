/**
 * 应用导航配置
 */

import React from 'react';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {createStackNavigator} from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

// 页面组件
import HomeScreen from '@/screens/HomeScreen';
import BoardScreen from '@/screens/BoardScreen';
import TaskScreen from '@/screens/TaskScreen';
import SearchScreen from '@/screens/SearchScreen';
import ProfileScreen from '@/screens/ProfileScreen';

// 类型定义
export type RootStackParamList = {
  MainTabs: undefined;
  Board: {boardId: string};
  Task: {taskId: string};
  Search: undefined;
  Profile: undefined;
};

export type MainTabParamList = {
  Home: undefined;
  Boards: undefined;
  Search: undefined;
  Notifications: undefined;
  Profile: undefined;
};

// 创建导航器
const Tab = createBottomTabNavigator<MainTabParamList>();
const Stack = createStackNavigator<RootStackParamList>();

// 主标签页导航
function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({route}) => ({
        tabBarIcon: ({focused, color, size}) => {
          let iconName = 'home';

          switch (route.name) {
            case 'Home':
              iconName = focused ? 'home' : 'home-outline';
              break;
            case 'Boards':
              iconName = focused ? 'view-column' : 'view-column-outline';
              break;
            case 'Search':
              iconName = focused ? 'magnify' : 'magnify';
              break;
            case 'Notifications':
              iconName = focused ? 'bell' : 'bell-outline';
              break;
            case 'Profile':
              iconName = focused ? 'account' : 'account-outline';
              break;
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#2196F3',
        tabBarInactiveTintColor: 'gray',
        headerShown: false,
      })}>
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Boards" component={HomeScreen} />
      <Tab.Screen name="Search" component={SearchScreen} />
      <Tab.Screen name="Notifications" component={HomeScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}

// 主应用导航
function AppNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: '#2196F3',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}>
      <Stack.Screen
        name="MainTabs"
        component={MainTabs}
        options={{headerShown: false}}
      />
      <Stack.Screen
        name="Board"
        component={BoardScreen}
        options={({route}) => ({
          title: '看板详情',
        })}
      />
      <Stack.Screen
        name="Task"
        component={TaskScreen}
        options={({route}) => ({
          title: '任务详情',
        })}
      />
      <Stack.Screen
        name="Search"
        component={SearchScreen}
        options={{title: '搜索'}}
      />
      <Stack.Screen
        name="Profile"
        component={ProfileScreen}
        options={{title: '个人资料'}}
      />
    </Stack.Navigator>
  );
}

export default AppNavigator;