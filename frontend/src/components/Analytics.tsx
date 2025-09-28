import React, { useState, useEffect } from 'react';
import { apiService, type Stats } from '../services/api';
import toast from 'react-hot-toast';
import {
  ChartBarIcon,
  DocumentTextIcon,
  CheckCircleIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  ArrowPathIcon,
  BuildingOfficeIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';

const Analytics: React.FC = () => {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  const loadStats = async () => {
    try {
      setLoading(true);
      const data = await apiService.getStats();
      setStats(data);
    } catch (error) {
      toast.error('Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  // Chart data preparation
  const categoryData = stats?.category_breakdown ? Object.entries(stats.category_breakdown).map(([name, value]) => ({
    name: name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
    value,
    fill: getCategoryColor(name)
  })) : [];

  const complexityData = stats?.complexity_breakdown ? Object.entries(stats.complexity_breakdown).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value,
    fill: getComplexityColor(name)
  })) : [];

  const dailyData = stats?.daily_stats ? stats.daily_stats.map(([date, count]) => ({
    date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    count
  })) : [];

  const companyData = stats?.company_breakdown ? Object.entries(stats.company_breakdown)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 10)
    .map(([name, value]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      value
    })) : [];

  function getCategoryColor(category: string) {
    const colors = {
      'big_tech_companies': '#3B82F6',
      'databases': '#10B981',
      'system_design': '#F59E0B',
      'cloud_infrastructure': '#8B5CF6',
      'security': '#EF4444',
      'ai_ml': '#EC4899',
      'networking': '#06B6D4',
      'algorithms': '#84CC16',
      'messaging_streaming': '#F97316'
    };
    return colors[category as keyof typeof colors] || '#6B7280';
  }

  function getComplexityColor(complexity: string) {
    const colors = {
      'beginner': '#10B981',
      'intermediate': '#F59E0B',
      'advanced': '#F97316',
      'expert': '#EF4444'
    };
    return colors[complexity as keyof typeof colors] || '#6B7280';
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mb-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
          </div>
          <p className="text-gray-600 text-lg font-medium">Loading analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header Section */}
      <div className="relative overflow-hidden bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="absolute inset-0">
          <div className="absolute top-0 left-0 w-96 h-96 bg-white/10 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse"></div>
          <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse animation-delay-2000"></div>
        </div>
        
        <div className="relative px-6 py-12">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-4xl font-bold text-white mb-2">
                  Analytics
                </h1>
                <p className="text-xl text-emerald-100">
                  Comprehensive insights into your system design topics
                </p>
              </div>
              <button
                onClick={loadStats}
                className="flex items-center px-6 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white font-semibold hover:bg-white/30 transition-all duration-200 transform hover:scale-105"
              >
                <ArrowPathIcon className="h-5 w-5 mr-2" />
                Refresh
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="px-6 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Summary Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="group relative">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-blue-600 rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-300"></div>
              <div className="relative bg-white/90 backdrop-blur-sm rounded-2xl p-6 border border-white/30 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 mb-1">Total Topics</p>
                    <p className="text-3xl font-bold text-gray-900">
                      {stats?.total_topics || 0}
                    </p>
                  </div>
                  <div className="p-3 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl">
                    <DocumentTextIcon className="h-6 w-6 text-white" />
                  </div>
                </div>
              </div>
            </div>

            <div className="group relative">
              <div className="absolute inset-0 bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-300"></div>
              <div className="relative bg-white/90 backdrop-blur-sm rounded-2xl p-6 border border-white/30 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 mb-1">Completed</p>
                    <p className="text-3xl font-bold text-gray-900">
                      {stats?.status_breakdown?.completed || 0}
                    </p>
                  </div>
                  <div className="p-3 bg-gradient-to-r from-green-500 to-emerald-600 rounded-xl">
                    <CheckCircleIcon className="h-6 w-6 text-white" />
                  </div>
                </div>
              </div>
            </div>

            <div className="group relative">
              <div className="absolute inset-0 bg-gradient-to-r from-amber-500 to-orange-600 rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-300"></div>
              <div className="relative bg-white/90 backdrop-blur-sm rounded-2xl p-6 border border-white/30 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 mb-1">Pending</p>
                    <p className="text-3xl font-bold text-gray-900">
                      {stats?.status_breakdown?.pending || 0}
                    </p>
                  </div>
                  <div className="p-3 bg-gradient-to-r from-amber-500 to-orange-600 rounded-xl">
                    <ClockIcon className="h-6 w-6 text-white" />
                  </div>
                </div>
              </div>
            </div>

            <div className="group relative">
              <div className="absolute inset-0 bg-gradient-to-r from-red-500 to-rose-600 rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-300"></div>
              <div className="relative bg-white/90 backdrop-blur-sm rounded-2xl p-6 border border-white/30 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 mb-1">Failed</p>
                    <p className="text-3xl font-bold text-gray-900">
                      {stats?.status_breakdown?.failed || 0}
                    </p>
                  </div>
                  <div className="p-3 bg-gradient-to-r from-red-500 to-rose-600 rounded-xl">
                    <ExclamationTriangleIcon className="h-6 w-6 text-white" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Charts Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            {/* Topics by Category */}
            <div className="group relative">
              <div className="absolute inset-0 bg-gradient-to-r from-white to-blue-50 rounded-3xl blur opacity-50 group-hover:opacity-70 transition duration-300"></div>
              <div className="relative bg-white/90 backdrop-blur-sm rounded-3xl p-8 border border-white/30 shadow-xl">
                <div className="flex items-center mb-6">
                  <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg mr-3">
                    <ChartBarIcon className="h-6 w-6 text-white" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900">Topics by Category</h2>
                </div>
                <div className="h-80">
                  {categoryData.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={categoryData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, percent }: any) => `${name} ${(percent * 100).toFixed(0)}%`}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {categoryData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.fill} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="flex items-center justify-center h-full text-gray-500">
                      <div className="text-center">
                        <ChartBarIcon className="h-12 w-12 mx-auto mb-2 text-gray-400" />
                        <p>No category data available</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Topics by Complexity */}
            <div className="group relative">
              <div className="absolute inset-0 bg-gradient-to-r from-white to-purple-50 rounded-3xl blur opacity-50 group-hover:opacity-70 transition duration-300"></div>
              <div className="relative bg-white/90 backdrop-blur-sm rounded-3xl p-8 border border-white/30 shadow-xl">
                <div className="flex items-center mb-6">
                  <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg mr-3">
                    <AcademicCapIcon className="h-6 w-6 text-white" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900">Topics by Complexity</h2>
                </div>
                <div className="h-80">
                  {complexityData.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={complexityData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="value" fill="#8884d8" />
                      </BarChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="flex items-center justify-center h-full text-gray-500">
                      <div className="text-center">
                        <AcademicCapIcon className="h-12 w-12 mx-auto mb-2 text-gray-400" />
                        <p>No complexity data available</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Daily Activity */}
          <div className="group relative mb-8">
            <div className="absolute inset-0 bg-gradient-to-r from-white to-emerald-50 rounded-3xl blur opacity-50 group-hover:opacity-70 transition duration-300"></div>
            <div className="relative bg-white/90 backdrop-blur-sm rounded-3xl p-8 border border-white/30 shadow-xl">
              <div className="flex items-center mb-6">
                <div className="p-2 bg-gradient-to-r from-emerald-500 to-teal-600 rounded-lg mr-3">
                  <ChartBarIcon className="h-6 w-6 text-white" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Daily Activity</h2>
              </div>
              <div className="h-80">
                {dailyData.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={dailyData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Area type="monotone" dataKey="count" stroke="#10B981" fill="#10B981" fillOpacity={0.3} />
                    </AreaChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="flex items-center justify-center h-full text-gray-500">
                    <div className="text-center">
                      <ChartBarIcon className="h-12 w-12 mx-auto mb-2 text-gray-400" />
                      <p>No daily activity data available</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Top Companies */}
          <div className="group relative">
            <div className="absolute inset-0 bg-gradient-to-r from-white to-orange-50 rounded-3xl blur opacity-50 group-hover:opacity-70 transition duration-300"></div>
            <div className="relative bg-white/90 backdrop-blur-sm rounded-3xl p-8 border border-white/30 shadow-xl">
              <div className="flex items-center mb-6">
                <div className="p-2 bg-gradient-to-r from-orange-500 to-red-600 rounded-lg mr-3">
                  <BuildingOfficeIcon className="h-6 w-6 text-white" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Top Companies</h2>
              </div>
              <div className="space-y-4">
                {companyData.length > 0 ? (
                  companyData.map((company, index) => (
                    <div key={company.name} className="flex items-center justify-between p-4 bg-gradient-to-r from-orange-50 to-red-50 rounded-xl border border-orange-200">
                      <div className="flex items-center">
                        <div className="w-8 h-8 bg-gradient-to-r from-orange-500 to-red-600 rounded-full flex items-center justify-center text-white font-bold text-sm mr-4">
                          {index + 1}
                        </div>
                        <span className="font-semibold text-gray-900">{company.name}</span>
                      </div>
                      <div className="flex items-center">
                        <div className="w-32 bg-gray-200 rounded-full h-2 mr-3">
                          <div 
                            className="bg-gradient-to-r from-orange-500 to-red-600 h-2 rounded-full transition-all duration-500"
                            style={{ width: `${(company.value / Math.max(...companyData.map(c => c.value))) * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium text-gray-600">{company.value}</span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="flex items-center justify-center py-12 text-gray-500">
                    <div className="text-center">
                      <BuildingOfficeIcon className="h-12 w-12 mx-auto mb-2 text-gray-400" />
                      <p>No company data available</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;