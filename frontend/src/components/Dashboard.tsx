import React, { useState, useEffect } from 'react';
import { apiService, type ProcessingStatus } from '../services/api';
import toast from 'react-hot-toast';
import { 
  DocumentTextIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ChartBarIcon,
  SparklesIcon,
  EyeIcon,
  BuildingOfficeIcon,
  ServerIcon,
  RocketLaunchIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline';
import { Button } from './ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/Card';
import { ProgressBar, Skeleton, LoadingSpinner } from './ui/LoadingStates';
import { useNavigate } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [topics, setTopics] = useState<string>('');
  const [batchSize, setBatchSize] = useState<number>(5);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [status, setStatus] = useState<ProcessingStatus | null>(null);

  useEffect(() => {
    console.log('Processing Status', status);
    console.log('is_processing', isProcessing);
  }, [status, isProcessing]);
  const [stats, setStats] = useState<any>(null);
  const [recentTopics, setRecentTopics] = useState<any[]>([]);
  const [loadingStats, setLoadingStats] = useState(true);

  // Load dashboard data
  useEffect(() => {
    loadDashboardData();
  }, []);

  // Poll for status updates when processing
  useEffect(() => {
    let interval: number;
    if (isProcessing) {
      interval = setInterval(() => {
        loadStatus();
      }, 2000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isProcessing]);

  const loadDashboardData = async () => {
    setLoadingStats(true);
    try {
      const [statsData, topicsData] = await Promise.all([
        apiService.getStats(),
        apiService.getTopics(0, 5)
      ]);
      
      setStats(statsData);
      setRecentTopics(topicsData.topics || []);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoadingStats(false);
    }
  };

  const loadStatus = async () => {
    try {
      const data = await apiService.getStatus();
      setStatus(data);
      if (!data.is_processing) {
        setIsProcessing(false);
        console.error('Failed to load status:');
        loadDashboardData(); // Refresh dashboard data after processing
      }
    } catch (error) {
      console.error('Failed to load status:', error);
    }
  };

  const handleGenerateTopics = async () => {
    if (!topics.trim()) {
      toast.error('Please enter at least one topic');
      return;
    }

    const topicList = topics.split('\n').filter(t => t.trim());
    if (topicList.length === 0) {
      toast.error('Please enter valid topics');
      return;
    }

    try {
      setIsProcessing(true);
      await apiService.createTopics(topicList, batchSize);
      toast.success(`Started processing ${topicList.length} topics`);
      setTopics(''); // Clear the input
      loadStatus();
    } catch (error) {
      console.error('Failed to start processing:', error);
      toast.error('Failed to start processing');
      setIsProcessing(false);
    }
  };

  const getProgressPercentage = () => {
    if (!status) return 0;
    const total = status.processed_topics + (status as any).failed_topics + status.skipped_topics;
    if (total === 0) return 0;
    return (status.processed_topics / total) * 100;
  };

  const eventLogEntries = status?.event_log ?? [];

  const statCards = [
    {
      title: 'Total Topics',
      value: stats?.total_topics || 0,
      icon: DocumentTextIcon,
      color: 'primary',
      subtext: 'All time',
      trend: '+12%'
    },
    {
      title: 'Completed',
      value: stats?.completed_topics || 0,
      icon: CheckCircleIcon,
      color: 'success',
      subtext: `${stats?.total_topics ? Math.round((stats.completed_topics / stats.total_topics) * 100) : 0}% success rate`,
      trend: '+5%'
    },
    {
      title: 'Processing',
      value: isProcessing ? 'Active' : 'Idle',
      icon: ClockIcon,
      color: 'warning',
      subtext: 'Ready to process',
      trend: null
    },
    {
      title: 'Skipped',
      value: stats?.pending_topics || 0,
      icon: ExclamationTriangleIcon,
      color: 'error',
      subtext: 'Already exist',
      trend: null
    }
  ];

  return (
    <div className="min-h-screen p-4 md:p-6 lg:p-8">
      {/* Animated Background */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-secondary-50 dark:from-gray-950 dark:via-gray-900 dark:to-black" />
        <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-primary-400/20 dark:bg-primary-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-secondary-400/20 dark:bg-secondary-500/10 rounded-full blur-3xl animate-pulse animation-delay-2000" />
      </div>

      {/* Header Section */}
      <div className="text-center mb-12 space-y-4 animate-fade-in-down">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-2xl shadow-2xl mb-4 animate-float">
          <DocumentTextIcon className="h-10 w-10 text-white" />
        </div>
        <h1 className="text-5xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 dark:from-primary-400 dark:to-secondary-400 bg-clip-text text-transparent">
          System Design Topic Generator
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed">
          Generate comprehensive system design topics using cutting-edge AI technology
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card 
              key={stat.title} 
              className={`relative overflow-hidden animate-fade-in-up animation-delay-${index * 100}`}
            >
              <CardContent className="p-6 bg-white dark:bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-200 dark:border-gray-700/50 hover:shadow-lg dark:hover:shadow-2xl transition-all duration-300">
                <div className="flex items-start justify-between">
                  <div className="space-y-2">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-300">
                      {stat.title}
                    </p>
                    <div className="flex items-baseline space-x-2">
                      {loadingStats ? (
                        <Skeleton className="h-8 w-20" />
                      ) : (
                        <>
                          <h3 className={`text-3xl font-bold ${
                            stat.color === 'primary' ? 'text-primary-600 dark:text-primary-400' :
                            stat.color === 'success' ? 'text-success-600 dark:text-success-400' :
                            stat.color === 'warning' ? 'text-warning-600 dark:text-warning-400' :
                            'text-error-600 dark:text-error-400'
                          }`}>
                            {stat.value}
                          </h3>
                          {stat.trend && (
                            <span className="text-sm font-medium text-success-600 dark:text-success-400">
                              {stat.trend}
                            </span>
                          )}
                        </>
                      )}
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {stat.subtext}
                    </p>
                  </div>
                  <div className={`p-3 rounded-xl ${
                    stat.color === 'primary' ? 'bg-primary-100 dark:bg-primary-500/20' :
                    stat.color === 'success' ? 'bg-success-100 dark:bg-success-500/20' :
                    stat.color === 'warning' ? 'bg-warning-100 dark:bg-warning-500/20' :
                    'bg-error-100 dark:bg-error-500/20'
                  }`}>
                    <Icon className={`h-6 w-6 ${
                      stat.color === 'primary' ? 'text-primary-600 dark:text-primary-400' :
                      stat.color === 'success' ? 'text-success-600 dark:text-success-400' :
                      stat.color === 'warning' ? 'text-warning-600 dark:text-warning-400' :
                      'text-error-600 dark:text-error-400'
                    }`} />
                  </div>
                </div>
                {/* Decorative gradient */}
                <div className={`absolute -right-8 -bottom-8 w-24 h-24 rounded-full blur-2xl ${
                  stat.color === 'primary' ? 'bg-primary-400/20 dark:bg-primary-500/10' :
                  stat.color === 'success' ? 'bg-success-400/20 dark:bg-success-500/10' :
                  stat.color === 'warning' ? 'bg-warning-400/20 dark:bg-warning-500/10' :
                  'bg-error-400/20 dark:bg-error-500/10'
                }`} />
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Topic Generation Section */}
        <div className="lg:col-span-2 space-y-6">
          {/* Enter Topics Card */}
          <Card className="relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-primary-400/20 to-secondary-400/20 dark:from-primary-500/10 dark:to-secondary-500/10 rounded-full blur-3xl" />
            <CardHeader className="bg-white dark:bg-gray-800/50 backdrop-blur-sm">
              <CardTitle className="flex items-center space-x-2 text-gray-900 dark:text-gray-100">
                <div className="p-2 bg-primary-100 dark:bg-primary-500/20 rounded-lg">
                  <DocumentTextIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                </div>
                <span>Enter Topics</span>
              </CardTitle>
              <CardDescription className="text-gray-600 dark:text-gray-300">
                Topic Names (one per line)
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6 bg-white dark:bg-gray-800/50 backdrop-blur-sm">
              <div className="relative">
                <textarea
                  value={topics}
                  onChange={(e) => setTopics(e.target.value)}
                  placeholder="How WhatsApp Group Calls Scale to Dozens&#10;How Redis Internally Works&#10;Designing a Distributed Cache Like Memcached"
                  className="input-field h-40 resize-none font-mono text-sm bg-gray-50 dark:bg-gray-900/50 border-gray-300 dark:border-gray-600"
                  disabled={isProcessing}
                />
                <div className="absolute bottom-2 right-2 text-xs text-gray-400">
                  {topics.split('\n').filter(t => t.trim()).length} topics
                </div>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                    Topics per API Call
                  </label>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">
                    Multiple API calls will run in parallel for faster processing
                  </p>
                  <div className="flex items-center space-x-2">
                    {[1, 3, 5].map((size) => (
                      <Button
                        key={size}
                        variant={batchSize === size ? 'primary' : 'outline'}
                        size="sm"
                        onClick={() => setBatchSize(size)}
                        disabled={isProcessing}
                        className="min-w-[60px]"
                      >
                        {size}
                      </Button>
                    ))}
                  </div>
                </div>
                
                <Button
                  variant="primary"
                  onClick={handleGenerateTopics}
                  disabled={isProcessing || !topics.trim()}
                  loading={isProcessing}
                  leftIcon={!isProcessing && <RocketLaunchIcon className="h-5 w-5" />}
                  className="w-full h-12 text-base font-semibold bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600"
                  animation="glow"
                >
                  Generate Topics
                </Button>
              </div>
            </CardContent>
          </Card>
          {/* Processing Status */}
          {isProcessing && status && (
            <Card className="relative overflow-hidden animate-fade-in-up bg-white dark:bg-gray-800/50 backdrop-blur-sm">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary-500 to-secondary-500 animate-shimmer" />
              <CardHeader>
                <CardTitle className="flex items-center space-x-2 text-gray-900 dark:text-gray-100">
                  <div className="p-2 bg-success-100 dark:bg-success-500/20 rounded-lg">
                    <ClockIcon className="h-6 w-6 text-success-600 dark:text-success-400 animate-spin" />
                  </div>
                  <span>Processing Status</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-2">
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-gray-600 dark:text-gray-400">Progress</span>
                    <span className="font-medium">{Math.round(getProgressPercentage())}%</span>
                  </div>
                  <ProgressBar progress={getProgressPercentage()} showPercentage={false} />
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-success-50 dark:bg-success-900/20 rounded-xl">
                    <div className="text-2xl font-bold text-success-600 dark:text-success-400">
                      {status.processed_topics}
                    </div>
                    <div className="text-xs text-success-600 dark:text-success-400">Completed</div>
                  </div>
                  <div className="text-center p-4 bg-warning-50 dark:bg-warning-900/20 rounded-xl">
                    <div className="text-2xl font-bold text-warning-600 dark:text-warning-400">
                      {status.skipped_topics}
                    </div>
                    <div className="text-xs text-warning-600 dark:text-warning-400">Skipped</div>
                  </div>
                  <div className="text-center p-4 bg-error-50 dark:bg-error-900/20 rounded-xl">
                    <div className="text-2xl font-bold text-error-600 dark:text-error-400">
                      {(status as any).failed_topics || 0}
                    </div>
                    <div className="text-xs text-error-600 dark:text-error-400">Failed</div>
                  </div>
                </div>

                {status.current_topic && (
                  <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-xl flex items-center space-x-3">
                    <LoadingSpinner size="sm" className="text-primary-500" />
                    <div className="text-sm text-gray-600 dark:text-gray-300">
                      <span className="font-medium">{status.current_topic}</span>
                    </div>
                  </div>
                )}

                {status && (
                  <div className="bg-white/60 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-700/60 rounded-xl p-4 shadow-inner max-h-64 overflow-y-auto space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-200 uppercase tracking-wide">
                        Recent Events
                      </h4>
                      <span className="text-xs text-gray-400">
                        Showing {Math.min(eventLogEntries.length, 20)} of {eventLogEntries.length}
                      </span>
                    </div>

                    {eventLogEntries.length === 0 ? (
                      <div className="text-xs text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800/80 border border-dashed border-gray-300 dark:border-gray-700 rounded-lg px-4 py-6 text-center">
                        No events yet. Start a topic batch to see real-time updates here.
                      </div>
                    ) : (
                      <ul className="space-y-2 text-xs text-gray-600 dark:text-gray-300">
                        {eventLogEntries.slice(-20).reverse().map((entry, index) => (
                          <li
                            key={`${entry}-${index}`}
                            className="px-3 py-2 bg-white dark:bg-gray-800/80 border border-gray-200 dark:border-gray-700/60 rounded-lg shadow-sm flex items-start space-x-3"
                          >
                            <span className="inline-flex h-5 w-5 items-center justify-center rounded-full bg-primary-100 text-primary-600 dark:bg-primary-500/20 dark:text-primary-300 text-[10px] font-semibold">
                              {eventLogEntries.length - index}
                            </span>
                            <span className="whitespace-pre-wrap leading-snug">
                              {entry}
                            </span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <Card className="relative overflow-hidden bg-white dark:bg-gray-800/50 backdrop-blur-sm">
            <div className="absolute -top-10 -right-10 w-32 h-32 bg-gradient-to-br from-secondary-400/20 to-primary-400/20 dark:from-secondary-500/10 dark:to-primary-500/10 rounded-full blur-3xl" />
            <CardHeader>
              <CardTitle className="flex items-center space-x-2 text-gray-900 dark:text-gray-100">
                <div className="p-2 bg-secondary-100 dark:bg-secondary-500/20 rounded-lg">
                  <SparklesIcon className="h-6 w-6 text-secondary-600 dark:text-secondary-400" />
                </div>
                <span>Quick Actions</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button 
                variant="outline" 
                className="w-full justify-start group"
                leftIcon={<EyeIcon className="h-4 w-4 group-hover:scale-110 transition-transform" />}
                onClick={() => navigate('/topics')}
              >
                View All Topics
              </Button>
              
              <Button 
                variant="outline" 
                className="w-full justify-start group"
                leftIcon={<ChartBarIcon className="h-4 w-4 group-hover:scale-110 transition-transform" />}
                onClick={() => navigate('/analytics')}
              >
                View Analytics
              </Button>
              
              <Button 
                variant="outline" 
                className="w-full justify-start group"
                leftIcon={<SparklesIcon className="h-4 w-4 group-hover:scale-110 transition-transform" />}
                onClick={() => navigate('/content-generator')}
              >
                Content Generator
              </Button>
            </CardContent>
          </Card>

          {/* Recent Topics */}
          <Card className="relative overflow-hidden bg-white dark:bg-gray-800/50 backdrop-blur-sm">
            <div className="absolute -bottom-10 -left-10 w-32 h-32 bg-gradient-to-br from-warning-400/20 to-error-400/20 dark:from-warning-500/10 dark:to-error-500/10 rounded-full blur-3xl" />
            <CardHeader>
              <CardTitle className="flex items-center space-x-2 text-gray-900 dark:text-gray-100">
                <div className="p-2 bg-warning-100 dark:bg-warning-500/20 rounded-lg">
                  <ClockIcon className="h-6 w-6 text-warning-600 dark:text-warning-400" />
                </div>
                <span>Recent Topics</span>
              </CardTitle>
              <CardDescription className="text-gray-600 dark:text-gray-300">
                {recentTopics.length > 0 && (
                  <Button
                    variant="link"
                    size="sm"
                    className="p-0 h-auto text-primary-600 dark:text-primary-400"
                    onClick={() => navigate('/topics')}
                  >
                    View All
                  </Button>
                )}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loadingStats ? (
                <div className="space-y-3">
                  {[1, 2, 3].map((i) => (
                    <Skeleton key={i} className="h-20 w-full" />
                  ))}
                </div>
              ) : recentTopics.length > 0 ? (
                <div className="space-y-3">
                  {recentTopics.slice(0, 5).map((topic, index) => (
                    <div 
                      key={topic.id} 
                      className={`p-4 bg-gray-50 dark:bg-gray-900/50 rounded-xl hover:shadow-md dark:hover:shadow-lg border border-gray-200 dark:border-gray-700/50 transition-all duration-200 cursor-pointer animate-fade-in-up animation-delay-${index * 100}`}
                      onClick={() => navigate(`/topics?search=${encodeURIComponent(topic.title)}`)}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className="text-sm font-semibold text-gray-900 dark:text-gray-100 line-clamp-2 mb-1">
                            {topic.title}
                          </h4>
                          <div className="flex items-center space-x-2 text-xs">
                            <span className={`badge badge-${topic.complexity_level === 'beginner' ? 'success' : topic.complexity_level === 'intermediate' ? 'warning' : 'error'}`}>
                              {topic.complexity_level}
                            </span>
                            <span className="text-gray-500 dark:text-gray-400">
                              {topic.company}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full mb-4">
                    <DocumentTextIcon className="h-8 w-8 text-gray-400" />
                  </div>
                  <p className="text-gray-500 dark:text-gray-400 font-medium">No topics yet</p>
                  <p className="text-sm text-gray-400 dark:text-gray-500">Generate your first topic above</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Additional Stats Section */}
      {stats && (
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="text-center p-6 bg-white dark:bg-gray-800/50 backdrop-blur-sm hover:shadow-lg dark:hover:shadow-2xl transition-all duration-300 animate-fade-in-up">
            <AcademicCapIcon className="h-12 w-12 text-primary-500 dark:text-primary-400 mx-auto mb-3" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Avg. Difficulty</h3>
            <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">
              {stats.avg_difficulty || '7.2'}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Out of 10</p>
          </Card>

          <Card className="text-center p-6 bg-white dark:bg-gray-800/50 backdrop-blur-sm hover:shadow-lg dark:hover:shadow-2xl transition-all duration-300 animate-fade-in-up animation-delay-100">
            <BuildingOfficeIcon className="h-12 w-12 text-secondary-500 dark:text-secondary-400 mx-auto mb-3" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Categories</h3>
            <p className="text-3xl font-bold text-secondary-600 dark:text-secondary-400">
              {Object.keys(stats.category_breakdown || {}).length || 12}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Unique categories</p>
          </Card>

          <Card className="text-center p-6 bg-white dark:bg-gray-800/50 backdrop-blur-sm hover:shadow-lg dark:hover:shadow-2xl transition-all duration-300 animate-fade-in-up animation-delay-200">
            <ServerIcon className="h-12 w-12 text-success-500 dark:text-success-400 mx-auto mb-3" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Companies</h3>
            <p className="text-3xl font-bold text-success-600 dark:text-success-400">
              {Object.keys(stats.company_breakdown || {}).length || 25}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Tech companies</p>
          </Card>
        </div>
      )}
    </div>
  );
};

export default Dashboard;