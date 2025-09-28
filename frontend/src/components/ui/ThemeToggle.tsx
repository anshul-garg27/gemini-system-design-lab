import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';
import { SunIcon, MoonIcon, ComputerDesktopIcon } from '@heroicons/react/24/outline';
import { Button } from './Button';

export const ThemeToggle: React.FC = () => {
  const { theme, setTheme } = useTheme();

  const themes = [
    { value: 'light', icon: SunIcon, label: 'Light' },
    { value: 'dark', icon: MoonIcon, label: 'Dark' },
    { value: 'system', icon: ComputerDesktopIcon, label: 'System' },
  ] as const;

  return (
    <div className="flex items-center space-x-1 bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
      {themes.map(({ value, icon: Icon, label }) => (
        <Button
          key={value}
          variant={theme === value ? 'primary' : 'ghost'}
          size="sm"
          onClick={() => setTheme(value)}
          className="px-3"
          title={`Switch to ${label} theme`}
        >
          <Icon className="h-4 w-4" />
        </Button>
      ))}
    </div>
  );
};
