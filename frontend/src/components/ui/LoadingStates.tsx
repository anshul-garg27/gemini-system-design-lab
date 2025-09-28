import React from 'react';
import { cn } from '../../lib/utils';

interface SkeletonProps {
  className?: string;
  lines?: number;
}

export const Skeleton: React.FC<SkeletonProps> = ({ className, lines = 1 }) => {
  if (lines === 1) {
    return <div className={cn("animate-pulse bg-gray-200 dark:bg-gray-700 rounded", className)} />;
  }

  return (
    <div className="space-y-2">
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className={cn(
            "animate-pulse bg-gray-200 dark:bg-gray-700 rounded",
            i === lines - 1 ? "w-3/4" : "w-full",
            className
          )}
        />
      ))}
    </div>
  );
};

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ size = 'md', className }) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
  };

  return (
    <div className={cn("animate-spin", sizeClasses[size], className)}>
      <svg className="w-full h-full" fill="none" viewBox="0 0 24 24">
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
    </div>
  );
};

interface ProgressBarProps {
  progress: number;
  className?: string;
  showPercentage?: boolean;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ 
  progress, 
  className, 
  showPercentage = false 
}) => {
  return (
    <div className={cn("w-full", className)}>
      <div className="flex justify-between items-center mb-1">
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Progress</span>
        {showPercentage && (
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            {Math.round(progress)}%
          </span>
        )}
      </div>
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
        <div
          className="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full transition-all duration-300 ease-out"
          style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
        />
      </div>
    </div>
  );
};
