/**
 * 应用主题配置
 */

import {DefaultTheme} from 'react-native-paper';

export const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#2196F3',
    accent: '#FF4081',
    background: '#F5F5F5',
    surface: '#FFFFFF',
    error: '#F44336',
    text: '#212121',
    disabled: '#9E9E9E',
    placeholder: '#757575',
    backdrop: 'rgba(0, 0, 0, 0.5)',
    notification: '#FF4081',
    
    // 自定义颜色
    success: '#4CAF50',
    warning: '#FF9800',
    info: '#2196F3',
    
    // 看板列颜色
    columnTodo: '#FFEBEE',
    columnDoing: '#FFF3E0',
    columnDone: '#E8F5E9',
    
    // 标签颜色
    tagUrgent: '#FF4444',
    tagImportant: '#FFAA00',
    tagRoutine: '#44AA44',
    tagLongTerm: '#4488FF',
    tagBug: '#FF44AA',
    tagFeature: '#AA44FF',
  },
  roundness: 8,
  fonts: {
    ...DefaultTheme.fonts,
    regular: {
      fontFamily: 'System',
      fontWeight: '400' as '400',
    },
    medium: {
      fontFamily: 'System',
      fontWeight: '500' as '500',
    },
    light: {
      fontFamily: 'System',
      fontWeight: '300' as '300',
    },
    thin: {
      fontFamily: 'System',
      fontWeight: '100' as '100',
    },
  },
  animation: {
    scale: 1.0,
  },
};

export default theme;