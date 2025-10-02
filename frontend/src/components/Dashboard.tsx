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
import { Skeleton } from './ui/LoadingStates';
import { useNavigate } from 'react-router-dom';
import { ProcessingStatus as ProcessingStatusComponent } from './ProcessingStatus';

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


  const statCards = [
    {
      title: 'Total Topics',
      value: stats?.total_topics || 0,
      icon: DocumentTextIcon,
      color: 'primary',
      subtext: 'All time',
      trend: stats?.total_topics > 0 ? '+12%' : null
    },
    {
      title: 'Completed',
      value: stats?.completed_topics || 0,
      icon: CheckCircleIcon,
      color: 'success',
      subtext: `${stats?.total_topics ? Math.round((stats.completed_topics / stats.total_topics) * 100) : 0}% success rate`,
      trend: stats?.completed_topics > 0 ? '+5%' : null
    },
    {
      title: 'Processing',
      value: isProcessing ? 'Active' : 'Idle',
      icon: ClockIcon,
      color: isProcessing ? 'warning' : 'neutral',
      subtext: isProcessing ? 'In progress' : 'Ready to process',
      trend: null
    },
    {
      title: 'Failed',
      value: stats?.failed_topics || 0,
      icon: ExclamationTriangleIcon,
      color: (stats?.failed_topics || 0) > 0 ? 'error' : 'neutral',
      subtext: 'Needs retry',
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

      {/* Header Section - Improved spacing and hierarchy */}
      <div className="text-center mb-10 space-y-3 animate-fade-in-down">
        <div className="inline-flex items-center justify-center w-16 h-16 gradient-brand rounded-2xl shadow-lg mb-3 animate-float">
          <DocumentTextIcon className="h-8 w-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-primary-700 to-primary-600 dark:from-primary-300 dark:to-primary-400 bg-clip-text text-transparent">
          System Design Topic Generator
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Generate comprehensive system design topics using AI
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card 
              key={stat.title} 
              className={`relative overflow-hidden animate-fade-in-up animation-delay-${index * 100} group cursor-pointer`}
            >
              <CardContent className="p-6 bg-white dark:bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-200 dark:border-gray-700/50 hover:shadow-xl dark:hover:shadow-2xl hover:border-primary-300 dark:hover:border-primary-600 transition-all duration-300 hover:-translate-y-1">
                <div className="flex items-start justify-between">
                  <div className="space-y-2 flex-1">
                    <p className="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
                      {stat.title}
                    </p>
                    <div className="flex items-baseline space-x-2">
                      {loadingStats ? (
                        <Skeleton className="h-10 w-24" />
                      ) : (
                        <>
                          <h3 className={`text-4xl font-extrabold tabular-nums ${
                            stat.color === 'primary' ? 'text-primary-600 dark:text-primary-400' :
                            stat.color === 'success' ? 'text-success-600 dark:text-success-400' :
                            stat.color === 'warning' ? 'text-warning-600 dark:text-warning-400' :
                            stat.color === 'error' ? 'text-error-600 dark:text-error-400' :
                            'text-gray-600 dark:text-gray-400'
                          }`}>
                            {stat.value}
                          </h3>
                          {stat.trend && (
                            <span className="text-xs font-bold text-success-600 dark:text-success-400 bg-success-50 dark:bg-success-900/30 px-1.5 py-0.5 rounded">
                              {stat.trend}
                            </span>
                          )}
                        </>
                      )}
                    </div>
                    <p className="text-xs text-gray-600 dark:text-gray-400 font-medium">
                      {stat.subtext}
                    </p>
                  </div>
                  <div className={`p-3 rounded-xl transition-transform group-hover:scale-110 ${
                    stat.color === 'primary' ? 'bg-primary-100 dark:bg-primary-500/20' :
                    stat.color === 'success' ? 'bg-success-100 dark:bg-success-500/20' :
                    stat.color === 'warning' ? 'bg-warning-100 dark:bg-warning-500/20' :
                    stat.color === 'error' ? 'bg-error-100 dark:bg-error-500/20' :
                    'bg-gray-100 dark:bg-gray-500/20'
                  }`}>
                    <Icon className={`h-7 w-7 ${
                      stat.color === 'primary' ? 'text-primary-600 dark:text-primary-400' :
                      stat.color === 'success' ? 'text-success-600 dark:text-success-400' :
                      stat.color === 'warning' ? 'text-warning-600 dark:text-warning-400' :
                      stat.color === 'error' ? 'text-error-600 dark:text-error-400' :
                      'text-gray-600 dark:text-gray-400'
                    }`} />
                  </div>
                </div>
                {/* Decorative gradient */}
                <div className={`absolute -right-8 -bottom-8 w-24 h-24 rounded-full blur-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 ${
                  stat.color === 'primary' ? 'bg-primary-400/30 dark:bg-primary-500/20' :
                  stat.color === 'success' ? 'bg-success-400/30 dark:bg-success-500/20' :
                  stat.color === 'warning' ? 'bg-warning-400/30 dark:bg-warning-500/20' :
                  stat.color === 'error' ? 'bg-error-400/30 dark:bg-error-500/20' :
                  'bg-gray-400/20 dark:bg-gray-500/10'
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
                  className="input-field h-40 resize-none font-mono text-sm bg-gray-50 dark:bg-gray-900/50 border-2 border-gray-300 dark:border-gray-600 focus:border-primary-500 dark:focus:border-primary-500 transition-colors"
                  disabled={isProcessing}
                />
                <div className="absolute bottom-3 right-3 text-xs font-semibold text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 px-2 py-1 rounded shadow-sm">
                  {topics.split('\n').filter(t => t.trim()).length} {topics.split('\n').filter(t => t.trim()).length === 1 ? 'topic' : 'topics'}
                </div>
              </div>
              
              <div className="space-y-4">
                <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                  <label className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-2 block flex items-center gap-2">
                    <SparklesIcon className="h-4 w-4 text-primary-500" />
                    Topics per API Call
                  </label>
                  <p className="text-xs text-gray-600 dark:text-gray-400 mb-3 leading-relaxed">
                    Multiple API calls run in parallel for faster processing. Higher values = faster but more API usage.
                  </p>
                  <div className="flex items-center space-x-2">
                    {[1, 3, 5].map((size) => (
                      <Button
                        key={size}
                        variant={batchSize === size ? 'primary' : 'outline'}
                        size="sm"
                        onClick={() => setBatchSize(size)}
                        disabled={isProcessing}
                        className={`min-w-[70px] font-bold transition-all ${
                          batchSize === size ? 'ring-2 ring-primary-400 ring-offset-2 dark:ring-offset-gray-800' : ''
                        }`}
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
                  className="w-full h-14 text-lg font-bold gradient-primary-cta shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all"
                  animation="glow"
                >
                  {isProcessing ? 'Processing...' : 'Generate Topics'}
                </Button>
              </div>
            </CardContent>
          </Card>
          {/* Processing Status */}
          <ProcessingStatusComponent />
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
                <div className="space-y-2">
                  {recentTopics.slice(0, 5).map((topic, index) => (
                    <div 
                      key={topic.id} 
                      className={`p-4 bg-gradient-to-r from-gray-50 to-gray-100/50 dark:from-gray-900/50 dark:to-gray-800/30 rounded-lg hover:shadow-md dark:hover:shadow-lg border border-gray-200 dark:border-gray-700/50 hover:border-primary-300 dark:hover:border-primary-700 transition-all duration-200 cursor-pointer animate-fade-in-up animation-delay-${index * 100} group`}
                      onClick={() => navigate(`/topics?search=${encodeURIComponent(topic.title)}`)}
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div className="flex-1 min-w-0">
                          <h4 className="text-sm font-bold text-gray-900 dark:text-gray-100 line-clamp-2 mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                            {topic.title}
                          </h4>
                          <div className="flex items-center gap-2 text-xs flex-wrap">
                            <span className={`badge ${topic.complexity_level === 'beginner' ? 'badge-success' : topic.complexity_level === 'intermediate' ? 'badge-warning' : 'bg-error-100 text-error-800 dark:bg-error-900 dark:text-error-200'} font-semibold capitalize`}>
                              {topic.complexity_level}
                            </span>
                            {topic.company && (
                              <span className="text-gray-600 dark:text-gray-400 font-medium flex items-center gap-1">
                                <BuildingOfficeIcon className="h-3 w-3" />
                                {topic.company}
                              </span>
                            )}
                          </div>
                        </div>
                        <ChartBarIcon className="h-4 w-4 text-gray-400 group-hover:text-primary-500 transition-colors flex-shrink-0" />
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-primary-100 to-secondary-100 dark:from-primary-900/30 dark:to-secondary-900/30 rounded-2xl mb-4 animate-pulse">
                    <DocumentTextIcon className="h-10 w-10 text-primary-500 dark:text-primary-400" />
                  </div>
                  <p className="text-gray-700 dark:text-gray-300 font-bold text-lg mb-1">No topics yet</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">Generate your first topic to get started</p>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => document.querySelector('textarea')?.focus()}
                    leftIcon={<RocketLaunchIcon className="h-4 w-4" />}
                    className="mx-auto"
                  >
                    Start Creating
                  </Button>
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