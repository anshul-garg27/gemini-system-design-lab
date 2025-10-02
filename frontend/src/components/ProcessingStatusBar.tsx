import React, { useState, useEffect } from 'react';
import { apiService, type TopicProcessingStatus } from '../services/api';
import { LoadingSpinner } from './ui/LoadingStates';

export const ProcessingStatusBar: React.FC = () => {
  const [status, setStatus] = useState<TopicProcessingStatus | null>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await apiService.getProcessingStatus();
        setStatus(data);
      } catch (err) {
        console.error('Error fetching processing status:', err);
      }
    };

    // Initial fetch
    fetchStatus();

    // Poll every 3 seconds when processing is active
    const interval = setInterval(() => {
      fetchStatus();
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  if (!status || !status.show_status) {
    return null;
  }

  const progress = status.total_count > 0 
    ? ((status.completed_count + status.failed_count) / status.total_count) * 100 
    : 0;

  return (
    <div className="fixed top-0 left-0 right-0 z-50 bg-blue-600 dark:bg-blue-800 text-white shadow-lg animate-slide-down">
      <div className="container mx-auto px-4 py-2">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <LoadingSpinner size="sm" className="text-white" />
              <span className="font-medium">Processing Topics</span>
            </div>
            
            <div className="hidden sm:flex items-center gap-4">
              <span className="opacity-90">
                {status.pending_count} pending
              </span>
              <span className="opacity-90">
                {status.processing_count} processing
              </span>
              <span className="opacity-90">
                {status.completed_count} completed
              </span>
              {status.failed_count > 0 && (
                <span className="text-red-200">
                  {status.failed_count} failed
                </span>
              )}
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div className="w-32 bg-blue-800 dark:bg-blue-900 rounded-full h-2 overflow-hidden">
                <div 
                  className="h-full bg-white transition-all duration-500 ease-out"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <span className="text-xs font-medium">{Math.round(progress)}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Add these styles to your global CSS or Tailwind config
// @keyframes slide-down {
//   from { transform: translateY(-100%); }
//   to { transform: translateY(0); }
// }
// .animate-slide-down {
//   animation: slide-down 0.3s ease-out;
// }
