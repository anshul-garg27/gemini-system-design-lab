import React, { useState } from 'react';
import { 
  CheckCircleIcon, 
  ExclamationTriangleIcon, 
  XCircleIcon, 
  ClockIcon,
  ArrowPathIcon,
  InformationCircleIcon,
  ChartBarIcon,
  KeyIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { cn } from '../lib/utils';

interface APIKeyStatus {
  key_index: number;
  key_preview: string;
  status: 'healthy' | 'rate_limited' | 'quota_exceeded' | 'error';
  last_checked: string;
  error_message?: string;
  usage_count: number;
  quota_info?: any;
}

interface HealthCheckResponse {
  total_keys: number;
  healthy_keys: number;
  rate_limited_keys: number;
  quota_exceeded_keys: number;
  error_keys: number;
  last_check: string;
  api_keys: APIKeyStatus[];
  recommendations: string[];
}

const ApiHealthCheck: React.FC = () => {
  const [healthData, setHealthData] = useState<HealthCheckResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastRefresh, setLastRefresh] = useState<Date | null>(null);
  const [hasChecked, setHasChecked] = useState(false);

  const fetchHealthData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/health/check');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setHealthData(data);
      setLastRefresh(new Date());
      setHasChecked(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch health data');
    } finally {
      setLoading(false);
    }
  };


  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'rate_limited':
        return <ClockIcon className="h-5 w-5 text-yellow-500" />;
      case 'quota_exceeded':
        return <ExclamationTriangleIcon className="h-5 w-5 text-orange-500" />;
      case 'error':
        return <XCircleIcon className="h-5 w-5 text-red-500" />;
      default:
        return <InformationCircleIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'rate_limited':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400';
      case 'quota_exceeded':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-400';
      case 'error':
        return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'Healthy';
      case 'rate_limited':
        return 'Rate Limited';
      case 'quota_exceeded':
        return 'Quota Exceeded';
      case 'error':
        return 'Error';
      default:
        return 'Unknown';
    }
  };

  const formatLastChecked = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  // Show initial state if no health check has been performed
  if (!hasChecked && !loading && !error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-6">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent dark:from-blue-400 dark:to-indigo-400">
                  API Health Check
                </h1>
                <p className="text-gray-600 dark:text-gray-400 mt-2">
                  Monitor your Gemini API keys status, quotas, and rate limits
                </p>
              </div>
            </div>
          </div>

          {/* Initial State Card */}
          <Card className="text-center">
            <CardContent className="p-12">
              <ShieldCheckIcon className="h-20 w-20 text-blue-500 mx-auto mb-6" />
              <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
                Ready to Check API Health
              </h2>
              <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
                Click the button below to perform a comprehensive health check on all your Gemini API keys. 
                This will test connectivity, check rate limits, verify quotas, and provide detailed status information.
              </p>
              <Button 
                onClick={fetchHealthData} 
                disabled={loading}
                variant="primary"
                size="lg"
                className="min-w-[200px]"
              >
                {loading ? (
                  <>
                    <ArrowPathIcon className="h-5 w-5 mr-2 animate-spin" />
                    Checking Health...
                  </>
                ) : (
                  <>
                    <ShieldCheckIcon className="h-5 w-5 mr-2" />
                    Check API Health
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-6">
        <div className="max-w-7xl mx-auto">
          <Card className="border-red-200 dark:border-red-800">
            <CardContent className="p-8 text-center">
              <XCircleIcon className="h-16 w-16 text-red-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                Health Check Failed
              </h2>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                {error}
              </p>
              <Button onClick={fetchHealthData} variant="primary">
                <ArrowPathIcon className="h-4 w-4 mr-2" />
                Try Again
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent dark:from-blue-400 dark:to-indigo-400">
                API Health Check
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-2">
                Monitor your Gemini API keys status, quotas, and rate limits
              </p>
            </div>
            <Button 
              onClick={fetchHealthData} 
              disabled={loading}
              variant="primary"
              className="min-w-[140px]"
            >
              {loading ? (
                <>
                  <ArrowPathIcon className="h-4 w-4 mr-2 animate-spin" />
                  Checking...
                </>
              ) : (
                <>
                  <ArrowPathIcon className="h-4 w-4 mr-2" />
                  Refresh
                </>
              )}
            </Button>
          </div>
          
          {lastRefresh && (
            <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
              Last updated: {lastRefresh.toLocaleString()}
            </p>
          )}
        </div>

        {healthData && (
          <>
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <Card className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 border-green-200 dark:border-green-700">
                <CardContent className="p-6">
                  <div className="flex items-center">
                    <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
                      <CheckCircleIcon className="h-6 w-6 text-green-600 dark:text-green-400" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-green-600 dark:text-green-400">Healthy</p>
                      <p className="text-2xl font-bold text-green-700 dark:text-green-300">
                        {healthData.healthy_keys}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-yellow-50 to-yellow-100 dark:from-yellow-900/20 dark:to-yellow-800/20 border-yellow-200 dark:border-yellow-700">
                <CardContent className="p-6">
                  <div className="flex items-center">
                    <div className="p-2 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg">
                      <ClockIcon className="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-yellow-600 dark:text-yellow-400">Rate Limited</p>
                      <p className="text-2xl font-bold text-yellow-700 dark:text-yellow-300">
                        {healthData.rate_limited_keys}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900/20 dark:to-orange-800/20 border-orange-200 dark:border-orange-700">
                <CardContent className="p-6">
                  <div className="flex items-center">
                    <div className="p-2 bg-orange-100 dark:bg-orange-900/30 rounded-lg">
                      <ExclamationTriangleIcon className="h-6 w-6 text-orange-600 dark:text-orange-400" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-orange-600 dark:text-orange-400">Quota Exceeded</p>
                      <p className="text-2xl font-bold text-orange-700 dark:text-orange-300">
                        {healthData.quota_exceeded_keys}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-red-50 to-red-100 dark:from-red-900/20 dark:to-red-800/20 border-red-200 dark:border-red-700">
                <CardContent className="p-6">
                  <div className="flex items-center">
                    <div className="p-2 bg-red-100 dark:bg-red-900/30 rounded-lg">
                      <XCircleIcon className="h-6 w-6 text-red-600 dark:text-red-400" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-red-600 dark:text-red-400">Errors</p>
                      <p className="text-2xl font-bold text-red-700 dark:text-red-300">
                        {healthData.error_keys}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Recommendations */}
            {healthData.recommendations.length > 0 && (
              <Card className="mb-8 border-blue-200 dark:border-blue-700">
                <CardHeader>
                  <CardTitle className="flex items-center text-blue-700 dark:text-blue-300">
                    <InformationCircleIcon className="h-5 w-5 mr-2" />
                    Recommendations
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {healthData.recommendations.map((recommendation, index) => (
                      <div key={index} className="flex items-start">
                        <span className="text-blue-500 mr-2">•</span>
                        <span className="text-gray-700 dark:text-gray-300">{recommendation}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* API Keys Details */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center text-gray-900 dark:text-gray-100">
                  <KeyIcon className="h-5 w-5 mr-2" />
                  API Keys Status ({healthData.total_keys} total)
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {healthData.api_keys.map((apiKey) => (
                    <div 
                      key={apiKey.key_index}
                      className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700"
                    >
                      <div className="flex items-center space-x-4">
                        <div className="flex items-center space-x-2">
                          {getStatusIcon(apiKey.status)}
                          <span className="font-medium text-gray-900 dark:text-gray-100">
                            Key #{apiKey.key_index}
                          </span>
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          {apiKey.key_preview}
                        </div>
                        <span className={cn(
                          "px-2 py-1 rounded-full text-xs font-medium",
                          getStatusColor(apiKey.status)
                        )}>
                          {getStatusText(apiKey.status)}
                        </span>
                      </div>
                      
                      <div className="flex items-center space-x-6 text-sm text-gray-500 dark:text-gray-400">
                        <div className="flex items-center space-x-1">
                          <ChartBarIcon className="h-4 w-4" />
                          <span>{apiKey.usage_count} uses</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <ClockIcon className="h-4 w-4" />
                          <span>{formatLastChecked(apiKey.last_checked)}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Additional Stats */}
            <Card className="mt-8">
              <CardHeader>
                <CardTitle className="flex items-center text-gray-900 dark:text-gray-100">
                  <ShieldCheckIcon className="h-5 w-5 mr-2" />
                  System Health Overview
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                      {Math.round((healthData.healthy_keys / healthData.total_keys) * 100)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      Health Score
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-600 dark:text-green-400 mb-2">
                      {healthData.total_keys}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      Total API Keys
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-purple-600 dark:text-purple-400 mb-2">
                      {healthData.api_keys.reduce((sum, key) => sum + key.usage_count, 0)}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      Total Usage
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </>
        )}
      </div>
    </div>
  );
};

export default ApiHealthCheck;
