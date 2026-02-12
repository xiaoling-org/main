/**
 * 小灵同学看板系统 - 手机APP
 * 主应用入口文件
 */

import React from 'react';
import {SafeAreaProvider} from 'react-native-safe-area-context';
import {Provider as PaperProvider} from 'react-native-paper';
import {NavigationContainer} from '@react-navigation/native';
import {StatusBar} from 'react-native';

// 状态管理
import {StoreProvider} from '@/store';

// 导航
import AppNavigator from '@/navigation/AppNavigator';

// 主题
import theme from '@/theme';

function App(): React.JSX.Element {
  return (
    <SafeAreaProvider>
      <PaperProvider theme={theme}>
        <StoreProvider>
          <NavigationContainer>
            <StatusBar
              barStyle="dark-content"
              backgroundColor={theme.colors.background}
            />
            <AppNavigator />
          </NavigationContainer>
        </StoreProvider>
      </PaperProvider>
    </SafeAreaProvider>
  );
}

export default App;