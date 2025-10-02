import React, { useState, useEffect } from 'react';
import { apiService, type TopicProcessingStatus } from '../services/api';
import { 
  ExclamationTriangleIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { ProgressBar, LoadingSpinner } from './ui/LoadingStates';

export const ProcessingStatus: React.FC = () => {
  const [status, setStatus] = useState<TopicProcessingStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await apiService.getProcessingStatus();
        setStatus(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching processing status:', err);
        setError('Failed to fetch processing status');
      } finally {
        setLoading(false);
      }
    };

    // Initial fetch
    fetchStatus();

    // Poll every 5 seconds when processing is active
    const interval = setInterval(() => {
      if (status?.is_processing || (status?.pending_count && status.pending_count > 0)) {
        fetchStatus();
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [status?.is_processing, status?.pending_count]);

  if (loading) {
    return null;
  }

  if (error) {
    return (
      <div className="mb-4 p-4 bg-red-50 dark:bg-red-900/20 rounded-lg flex items-center gap-2">
        <ExclamationTriangleIcon className="h-5 w-5 text-red-600 dark:text-red-400" />
        <div>
          <p className="font-medium text-red-900 dark:text-red-100">Error</p>
          <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
        </div>
      </div>
    );
  }

  if (!status || !status.show_status) {
    return null;
  }

  const progress = status.total_count > 0 
    ? ((status.completed_count + status.failed_count) / status.total_count) * 100 
    : 0;

  return (
    <Card className="mb-6 bg-white dark:bg-gray-800/50 backdrop-blur-sm animate-fade-in-up">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center space-x-2 text-gray-900 dark:text-gray-100">
            <div className="p-2 bg-primary-100 dark:bg-primary-500/20 rounded-lg">
              <ClockIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
            </div>
            <span>Topic Processing Status</span>
          </CardTitle>
          {status.is_processing && (
            <div className="flex items-center gap-2 px-3 py-1 bg-blue-100 dark:bg-blue-500/20 rounded-full">
              <LoadingSpinner size="sm" className="text-blue-600 dark:text-blue-400" />
              <span className="text-sm font-medium text-blue-600 dark:text-blue-400">Processing</span>
            </div>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Progress Bar */}
        <div className="space-y-2">
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-600 dark:text-gray-400">Progress</span>
            <span className="font-medium">{Math.round(progress)}%</span>
          </div>
          <ProgressBar progress={progress} showPercentage={false} />
          <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
            <span>{status.completed_count + status.failed_count} of {status.total_count} topics</span>
            <span>ETA: {status.pending_count > 0 ? `~${Math.ceil(status.pending_count / 5) * 2} min` : 'Complete'}</span>
          </div>
        </div>

        {/* Status Counts */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-xl">
            <ClockIcon className="h-6 w-6 text-yellow-600 dark:text-yellow-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
              {status.pending_count}
            </div>
            <div className="text-xs text-yellow-600 dark:text-yellow-400">Pending</div>
          </div>
          
          <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl">
            <div className="relative">
              <ClockIcon className="h-6 w-6 text-blue-600 dark:text-blue-400 mx-auto mb-2 animate-spin" />
            </div>
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
              {status.processing_count}
            </div>
            <div className="text-xs text-blue-600 dark:text-blue-400">Processing</div>
          </div>
          
          <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-xl">
            <CheckCircleIcon className="h-6 w-6 text-green-600 dark:text-green-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-green-600 dark:text-green-400">
              {status.completed_count}
            </div>
            <div className="text-xs text-green-600 dark:text-green-400">Completed</div>
          </div>
          
          <div className="text-center p-4 bg-red-50 dark:bg-red-900/20 rounded-xl">
            <XCircleIcon className="h-6 w-6 text-red-600 dark:text-red-400 mx-auto mb-2" />
            <div className="text-2xl font-bold text-red-600 dark:text-red-400">
              {status.failed_count}
            </div>
            <div className="text-xs text-red-600 dark:text-red-400">Failed</div>
          </div>
        </div>

        {/* Recent Failures */}
        {status.recent_failures.length > 0 && (
          <div className="mt-4 space-y-2">
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">Recent Failures</h4>
            <div className="space-y-2">
              {status.recent_failures.slice(0, 3).map((failure, idx) => (
                <div key={idx} className="p-3 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
                  <div className="flex items-start gap-2">
                    <ExclamationTriangleIcon className="h-4 w-4 text-red-600 dark:text-red-400 mt-0.5" />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-red-900 dark:text-red-100">{failure.title}</p>
                      <p className="text-xs text-red-700 dark:text-red-300 mt-1">
                        {failure.error_message}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
