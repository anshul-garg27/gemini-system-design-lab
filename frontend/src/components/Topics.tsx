import React, { useState, useEffect } from 'react';
import { apiService, type Topic } from '../services/api';
import toast from 'react-hot-toast';
import { 
  MagnifyingGlassIcon,
  FunnelIcon,
  EyeIcon,
  TrashIcon,
  ArrowPathIcon,
  DocumentTextIcon,
  CheckCircleIcon,
  ClockIcon,
  XMarkIcon,
  ClipboardDocumentIcon,
  ShareIcon,
  StarIcon,
  AcademicCapIcon,
  BuildingOfficeIcon,
  ChartBarIcon,
  CogIcon,
  TagIcon,
  LinkIcon,
  Squares2X2Icon,
  ListBulletIcon,
  ChevronUpIcon,
  ChevronDownIcon,
  AdjustmentsHorizontalIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';
import { Card, CardContent } from './ui/Card';
import { Button } from './ui/Button';

const Topics: React.FC = () => {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [filterComplexity, setFilterComplexity] = useState('');
  const [filterCompany, setFilterCompany] = useState('');
  const [selectedTopic, setSelectedTopic] = useState<Topic | null>(null);
  const [selectedTopics, setSelectedTopics] = useState<Set<number>>(new Set());
  const [sortBy, setSortBy] = useState<'title' | 'difficulty' | 'created_date' | 'company'>('created_date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [showFilters, setShowFilters] = useState(false);
  const [categories, setCategories] = useState<string[]>([]);
  const [companies, setCompanies] = useState<string[]>([]);
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [totalTopics, setTotalTopics] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  const loadTopics = async (page = currentPage, size = pageSize) => {
    try {
      setLoading(true);
      const offset = (page - 1) * size;
      
      // Fetch topics using API service
      const response = await apiService.getTopics(size, offset, searchTerm, {
        subcategory: filterCategory,
        status: filterStatus,
        complexity: filterComplexity,
        company: filterCompany,
        sortBy: sortBy,
        sortOrder: sortOrder
      });
      
      setTopics(response.topics || []);
      setTotalTopics(response.total_count || 0);
      setTotalPages(Math.ceil((response.total_count || 0) / size));
      
      // Extract unique categories and companies from current results
      // Note: For better UX, we could fetch all categories separately
      const uniqueCategories = [
        ...new Set(response.topics.map(topic => topic.subcategory).filter(Boolean))
      ];
      const uniqueCompanies = [...new Set(response.topics.map(topic => topic.company))];
      setCategories(uniqueCategories);
      setCompanies(uniqueCompanies);
    } catch (error) {
      toast.error('Failed to load topics');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTopics();
  }, []);

  // Handle page changes
  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    loadTopics(page, pageSize);
  };

  // Handle page size changes
  const handlePageSizeChange = (size: number) => {
    setPageSize(size);
    setCurrentPage(1); // Reset to first page
    loadTopics(1, size);
  };

  // Handle refresh
  const handleRefresh = () => {
    loadTopics(currentPage, pageSize);
  };

  // Handle search changes with debouncing
  const [searchTimeout, setSearchTimeout] = useState<number | null>(null);
  
  const handleSearchChange = (value: string) => {
    setSearchTerm(value);
    setCurrentPage(1); // Reset to first page
    
    // Clear existing timeout
    if (searchTimeout) {
      clearTimeout(searchTimeout);
    }
    
    // Set new timeout for debounced search
    const timeoutId = setTimeout(() => {
      loadTopics(1, pageSize);
    }, 500);
    
    setSearchTimeout(timeoutId);
  };

  // Handle filter changes
  const handleFilterChange = (filterType: string, value: string) => {
    switch (filterType) {
      case 'category':
        setFilterCategory(value);
        break;
      case 'status':
        setFilterStatus(value);
        break;
      case 'complexity':
        setFilterComplexity(value);
        break;
      case 'company':
        setFilterCompany(value);
        break;
    }
    setCurrentPage(1); // Reset to first page
    loadTopics(1, pageSize);
  };

  // Handle sort changes
  const handleSortChange = (field: 'title' | 'difficulty' | 'created_date' | 'company') => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('asc');
    }
    setCurrentPage(1); // Reset to first page
    loadTopics(1, pageSize);
  };

  // Clear all filters
  const clearAllFilters = () => {
    setSearchTerm('');
    setFilterCategory('');
    setFilterStatus('');
    setFilterComplexity('');
    setFilterCompany('');
    setCurrentPage(1);
    loadTopics(1, pageSize);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this topic?')) return;
    
    try {
      await apiService.deleteTopic(id);
      setTopics(topics.filter(topic => topic.id !== id));
      toast.success('Topic deleted successfully');
    } catch (error) {
      toast.error('Failed to delete topic');
    }
  };

  const handleBulkDelete = async () => {
    if (selectedTopics.size === 0) return;
    if (!confirm(`Are you sure you want to delete ${selectedTopics.size} topics?`)) return;
    
    try {
      const deletePromises = Array.from(selectedTopics).map(id => apiService.deleteTopic(id));
      await Promise.all(deletePromises);
      setTopics(topics.filter(topic => !selectedTopics.has(topic.id)));
      setSelectedTopics(new Set());
      toast.success(`${selectedTopics.size} topics deleted successfully`);
    } catch (error) {
      toast.error('Failed to delete some topics');
    }
  };

  const handleSelectAll = () => {
    if (selectedTopics.size === topics.length) {
      setSelectedTopics(new Set());
    } else {
      setSelectedTopics(new Set(topics.map(topic => topic.id)));
    }
  };

  const handleSelectTopic = (id: number) => {
    const newSelected = new Set(selectedTopics);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedTopics(newSelected);
  };

  const clearFilters = () => {
    setSearchTerm('');
    setFilterCategory('');
    setFilterStatus('');
    setFilterComplexity('');
    setFilterCompany('');
  };

  // Server-side filtering and sorting - no client-side logic needed

  const getComplexityBadgeClass = (complexity: string) => {
    switch (complexity.toLowerCase()) {
      case 'beginner': return 'bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 border-success-200 dark:border-success-700';
      case 'intermediate': return 'bg-warning-100 dark:bg-warning-900/20 text-warning-800 dark:text-warning-400 border-warning-200 dark:border-warning-700';
      case 'advanced': return 'bg-orange-100 dark:bg-orange-900/20 text-orange-800 dark:text-orange-400 border-orange-200 dark:border-orange-700';
      case 'expert': return 'bg-error-100 dark:bg-error-900/20 text-error-800 dark:text-error-400 border-error-200 dark:border-error-700';
      default: return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-700';
    }
  };

  const getStatusBadgeClass = (status: string | undefined) => {
    if (!status) return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-700';
    switch (status.toLowerCase()) {
      case 'completed': return 'bg-success-100 dark:bg-success-900/20 text-success-800 dark:text-success-400 border-success-200 dark:border-success-700';
      case 'pending': return 'bg-warning-100 dark:bg-warning-900/20 text-warning-800 dark:text-warning-400 border-warning-200 dark:border-warning-700';
      case 'failed': return 'bg-error-100 dark:bg-error-900/20 text-error-800 dark:text-error-400 border-error-200 dark:border-error-700';
      default: return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-700';
    }
  };

  const copyToClipboard = async (text: string, label: string) => {
    try {
      await navigator.clipboard.writeText(text);
      toast.success(`${label} copied to clipboard!`);
    } catch (err) {
      toast.error('Failed to copy to clipboard');
    }
  };

  const getDifficultyColor = (difficulty: number) => {
    if (difficulty <= 3) return 'text-success-600 dark:text-success-400 bg-success-100 dark:bg-success-900/20';
    if (difficulty <= 6) return 'text-warning-600 dark:text-warning-400 bg-warning-100 dark:bg-warning-900/20';
    if (difficulty <= 8) return 'text-orange-600 dark:text-orange-400 bg-orange-100 dark:bg-orange-900/20';
    return 'text-error-600 dark:text-error-400 bg-error-100 dark:bg-error-900/20';
  };

  const getComplexityColor = (complexity: string) => {
    switch (complexity.toLowerCase()) {
      case 'beginner': return 'text-primary-600 dark:text-primary-400 bg-primary-100 dark:bg-primary-900/20';
      case 'intermediate': return 'text-success-600 dark:text-success-400 bg-success-100 dark:bg-success-900/20';
      case 'advanced': return 'text-warning-600 dark:text-warning-400 bg-warning-100 dark:bg-warning-900/20';
      case 'expert': return 'text-error-600 dark:text-error-400 bg-error-100 dark:bg-error-900/20';
      default: return 'text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 dark:from-gray-950 dark:via-gray-900 dark:to-black flex items-center justify-center">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full mb-4 animate-pulse">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
          </div>
          <p className="text-gray-600 dark:text-gray-300 text-lg font-medium">Loading all topics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 dark:from-gray-950 dark:via-gray-900 dark:to-black">
      {/* Animated Background */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute top-0 left-0 w-[600px] h-[600px] bg-primary-400/20 dark:bg-primary-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-0 w-[600px] h-[600px] bg-secondary-400/20 dark:bg-secondary-500/10 rounded-full blur-3xl animate-pulse animation-delay-2000" />
      </div>

      {/* Header Section */}
      <div className="relative overflow-hidden bg-gradient-to-r from-primary-600 via-secondary-600 to-primary-700 dark:from-primary-800 dark:via-secondary-800 dark:to-primary-900">
        <div className="absolute inset-0 bg-black/10 dark:bg-black/20"></div>
        <div className="absolute inset-0">
          <div className="absolute top-0 left-0 w-96 h-96 bg-white/10 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse"></div>
          <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse animation-delay-2000"></div>
        </div>
        
        <div className="relative px-6 py-12">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-4xl font-bold text-white mb-2 gradient-text-primary">
                  Topics
                </h1>
                <p className="text-xl text-primary-100">
                  Manage and view generated system design topics
                </p>
              </div>
              <Button
                onClick={handleRefresh}
variant="ghost"
                className="bg-white/20 backdrop-blur-sm border-white/30 text-white hover:bg-white/30"
                leftIcon={<ArrowPathIcon className="h-5 w-5" />}
              >
                Refresh
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="px-6 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Enhanced Filters & Controls */}
          <Card className="mb-8 relative overflow-hidden animate-fade-in-up">
            <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-primary-400/20 to-secondary-400/20 dark:from-primary-500/10 dark:to-secondary-500/10 rounded-full blur-3xl" />
            <CardContent className="p-8">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                  <div className="p-2 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-lg mr-3">
                    <FunnelIcon className="h-6 w-6 text-white" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Filters & Search</h2>
                </div>
                <div className="flex items-center space-x-3">
                  <Button
                    onClick={() => setShowFilters(!showFilters)}
                    variant="outline"
                    size="sm"
                    leftIcon={<AdjustmentsHorizontalIcon className="h-5 w-5" />}
                  >
                    {showFilters ? 'Hide' : 'Show'} Advanced
                  </Button>
                  <Button
                    onClick={clearAllFilters}
                    variant="outline"
                    size="sm"
                    className="text-error-600 dark:text-error-400 border-error-300 dark:border-error-600 hover:bg-error-50 dark:hover:bg-error-900/20"
                    leftIcon={<XCircleIcon className="h-5 w-5" />}
                  >
                    Clear All
                  </Button>
                </div>
              </div>
              
              {/* Basic Filters */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                    Search Topics
                  </label>
                  <div className="relative">
                    <MagnifyingGlassIcon className="h-5 w-5 absolute left-4 top-4 text-gray-400 dark:text-gray-500" />
                    <input
                      type="text"
                      className="w-full pl-12 pr-4 py-3 bg-gray-50 dark:bg-gray-900/50 border border-gray-300 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 placeholder-gray-400 dark:placeholder-gray-500 text-gray-900 dark:text-gray-100"
                      placeholder="Search topics..."
                      value={searchTerm}
                      onChange={(e) => handleSearchChange(e.target.value)}
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                    Category
                  </label>
                  <select
                    className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-900/50 border border-gray-300 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 text-gray-900 dark:text-gray-100"
                    value={filterCategory}
                    onChange={(e) => handleFilterChange('category', e.target.value)}
                  >
                    <option value="">All Categories</option>
                    {categories.map(category => (
                      <option key={category} value={category}>
                        {category
                          .replace(/_/g, ' ')
                          .replace(/\b\w/g, l => l.toUpperCase())}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                    Status
                  </label>
                  <select
                    className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-900/50 border border-gray-300 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 text-gray-900 dark:text-gray-100"
                    value={filterStatus}
                    onChange={(e) => handleFilterChange('status', e.target.value)}
                  >
                    <option value="">All Statuses</option>
                    <option value="completed">Completed</option>
                    <option value="pending">Pending</option>
                    <option value="failed">Failed</option>
                  </select>
                </div>
              </div>

              {/* Advanced Filters */}
              {showFilters && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                      Complexity
                    </label>
                    <select
                      className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-900/50 border border-gray-300 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 text-gray-900 dark:text-gray-100"
                      value={filterComplexity}
                      onChange={(e) => handleFilterChange('complexity', e.target.value)}
                    >
                      <option value="">All Levels</option>
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                      <option value="expert">Expert</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                      Company
                    </label>
                    <select
                      className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-900/50 border border-gray-300 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 text-gray-900 dark:text-gray-100"
                      value={filterCompany}
                      onChange={(e) => handleFilterChange('company', e.target.value)}
                    >
                      <option value="">All Companies</option>
                      {companies.map(company => (
                        <option key={company} value={company}>
                          {company.charAt(0).toUpperCase() + company.slice(1)}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                      Sort By
                    </label>
                    <div className="flex space-x-2">
                      <select
                        className="flex-1 px-4 py-3 bg-gray-50 dark:bg-gray-900/50 border border-gray-300 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 text-gray-900 dark:text-gray-100"
                        value={sortBy}
                        onChange={(e) => handleSortChange(e.target.value as any)}
                      >
                        <option value="created_date">Date Created</option>
                        <option value="title">Title</option>
                        <option value="difficulty">Difficulty</option>
                        <option value="company">Company</option>
                      </select>
                      <button
                        onClick={() => handleSortChange(sortBy)}
                        className="px-3 py-3 bg-gray-50 dark:bg-gray-900/50 border border-gray-300 dark:border-gray-600 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
                      >
                        {sortOrder === 'asc' ? <ChevronUpIcon className="h-5 w-5" /> : <ChevronDownIcon className="h-5 w-5" />}
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* View Controls & Bulk Actions */}
              <div className="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Show:</span>
                    <select
                      value={pageSize}
                      onChange={(e) => handlePageSizeChange(Number(e.target.value))}
                      className="px-3 py-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900 dark:text-gray-100"
                    >
                      <option value={10}>10</option>
                      <option value={20}>20</option>
                      <option value={30}>30</option>
                      <option value={50}>50</option>
                    </select>
                    <span className="text-sm text-gray-600 dark:text-gray-400">per page</span>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">View:</span>
                    <button
                      onClick={() => setViewMode('grid')}
                      className={`p-2 rounded-lg transition-colors duration-200 ${
                        viewMode === 'grid' ? 'bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
                      }`}
                    >
                      <Squares2X2Icon className="h-5 w-5" />
                    </button>
                    <button
                      onClick={() => setViewMode('list')}
                      className={`p-2 rounded-lg transition-colors duration-200 ${
                        viewMode === 'list' ? 'bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700'
                      }`}
                    >
                      <ListBulletIcon className="h-5 w-5" />
                    </button>
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Showing {topics.length} topics (Page {currentPage} of {totalPages}) • Total: {totalTopics}
                  </div>
                </div>

                {selectedTopics.size > 0 && (
                  <div className="flex items-center space-x-3">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      {selectedTopics.size} selected
                    </span>
                    <Button
                      onClick={handleBulkDelete}
      variant="error"
                      size="sm"
                      leftIcon={<TrashIcon className="h-4 w-4" />}
                    >
                      Delete Selected
                    </Button>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Topics Grid/List */}
          <div className={`${viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' : 'space-y-4'}`}>
            {/* Select All Checkbox */}
            {topics.length > 0 && (
              <div className={`${viewMode === 'grid' ? 'col-span-full' : ''} mb-4`}>
                <label className="flex items-center space-x-3 p-4 bg-white dark:bg-gray-800/50 rounded-xl border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-200 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedTopics.size === topics.length && topics.length > 0}
                    onChange={handleSelectAll}
                    className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Select All ({topics.length} topics)
                  </span>
                </label>
              </div>
            )}

            {topics.map((topic) => (
              <Card 
                key={topic.id} 
                className={`group relative animate-fade-in-up hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 ${viewMode === 'list' ? 'flex items-center' : ''}`}
                variant="default"
              >
                <CardContent className={viewMode === 'list' ? 'p-4 flex-1' : 'p-6'}>
                  {/* Selection Checkbox */}
                  <div className="flex items-start space-x-3">
                    <input
                      type="checkbox"
                      checked={selectedTopics.has(topic.id)}
                      onChange={() => handleSelectTopic(topic.id)}
                      className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500 mt-1"
                    />
                    
                    <div className="flex-1">
                      <div className={`${viewMode === 'list' ? 'flex items-center justify-between' : ''}`}>
                        <div className={`${viewMode === 'list' ? 'flex-1' : ''}`}>
                          <h3 className={`font-bold text-gray-900 dark:text-gray-100 mb-2 ${viewMode === 'list' ? 'text-lg' : 'text-lg line-clamp-2'}`}>
                            {topic.title}
                          </h3>
                          <p className={`text-gray-600 dark:text-gray-400 mb-3 ${viewMode === 'list' ? 'text-sm line-clamp-1' : 'text-sm line-clamp-3'}`}>
                            {topic.description}
                          </p>
                        </div>

                        {viewMode === 'list' && (
                          <div className="flex items-center space-x-4 ml-4">
                            <div className="flex flex-wrap gap-2">
                              <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getComplexityBadgeClass(topic.complexity_level)}`}>
                                {topic.complexity_level}
                              </span>
                              <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getStatusBadgeClass(topic.processing_status)}`}>
                                {topic.processing_status}
                              </span>
                            </div>
                            <div className="text-sm text-gray-500 dark:text-gray-400">
                              <div className="font-medium">{topic.company}</div>
                              <div>{topic.difficulty}/10</div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <Button
                                onClick={() => setSelectedTopic(topic)}
                                variant="primary"
                                size="sm"
                                leftIcon={<EyeIcon className="h-4 w-4" />}
                              >
                                View
                              </Button>
                              <Button
                                onClick={() => handleDelete(topic.id)}
                variant="error"
                                size="sm"
                                leftIcon={<TrashIcon className="h-4 w-4" />}
                              >
                                Delete
                              </Button>
                            </div>
                          </div>
                        )}
                      </div>

                      {viewMode === 'grid' && (
                        <>
                          <div className="flex flex-wrap gap-2 mb-4">
                            <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getComplexityBadgeClass(topic.complexity_level)}`}>
                              {topic.complexity_level}
                            </span>
                            <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getStatusBadgeClass(topic.processing_status)}`}>
                              {topic.processing_status}
                            </span>
                          </div>

                          <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mb-4">
                            <span className="font-medium">{topic.company}</span>
                            <span>{topic.difficulty}/10</span>
                          </div>

                          <div className="flex items-center justify-between">
                            <Button
                              onClick={() => setSelectedTopic(topic)}
                              variant="primary"
                              size="sm"
                              leftIcon={<EyeIcon className="h-4 w-4" />}
                            >
                              View
                            </Button>
                            <Button
                              onClick={() => handleDelete(topic.id)}
              variant="error"
                              size="sm"
                              leftIcon={<TrashIcon className="h-4 w-4" />}
                            >
                              Delete
                            </Button>
                          </div>
                        </>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Pagination Controls */}
          {topics.length > 0 && totalPages > 1 && (
            <div className="flex items-center justify-between pt-8 border-t border-gray-200 dark:border-gray-700">
              <div className="flex items-center space-x-2">
                <Button
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 1}
                  variant="outline"
                  size="sm"
                >
                  Previous
                </Button>
                
                <div className="flex items-center space-x-1">
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    let pageNum;
                    if (totalPages <= 5) {
                      pageNum = i + 1;
                    } else if (currentPage <= 3) {
                      pageNum = i + 1;
                    } else if (currentPage >= totalPages - 2) {
                      pageNum = totalPages - 4 + i;
                    } else {
                      pageNum = currentPage - 2 + i;
                    }
                    
                    return (
                      <Button
                        key={pageNum}
                        onClick={() => handlePageChange(pageNum)}
                        variant={currentPage === pageNum ? 'primary' : 'outline'}
                        size="sm"
                        className="min-w-[40px]"
                      >
                        {pageNum}
                      </Button>
                    );
                  })}
                </div>
                
                <Button
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage === totalPages}
                  variant="outline"
                  size="sm"
                >
                  Next
                </Button>
              </div>
              
              <div className="text-sm text-gray-600 dark:text-gray-400">
                Page {currentPage} of {totalPages} • {totalTopics} total topics
              </div>
            </div>
          )}

          {topics.length === 0 && (
            <div className="text-center py-12">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-gray-400 to-gray-500 rounded-full mb-4">
                <DocumentTextIcon className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">No topics found</h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">Try adjusting your search or filter criteria</p>
              <Button
                onClick={clearFilters}
                variant="primary"
                size="lg"
              >
                Clear All Filters
              </Button>
            </div>
          )}
        </div>
      </div>

      {/* Enhanced Topic Detail Modal */}
      {selectedTopic && (
        <div className="fixed inset-0 bg-black/60 dark:bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
          <div className="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl w-full max-w-5xl max-h-[95vh] overflow-hidden relative transform scale-95 animate-scale-in border border-gray-200 dark:border-gray-700">
            {/* Header */}
            <div className="sticky top-0 bg-white/95 dark:bg-gray-900/95 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700 px-8 py-6 rounded-t-3xl">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h2 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-3 leading-tight gradient-text-primary">
                    {selectedTopic.title}
                  </h2>
                  <div className="flex flex-wrap gap-2 mb-4">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getComplexityColor(selectedTopic.complexity_level)}`}>
                      {selectedTopic.complexity_level}
                    </span>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(selectedTopic.difficulty)}`}>
                      Difficulty: {selectedTopic.difficulty}/10
                    </span>
                    <span className="px-3 py-1 rounded-full text-sm font-medium bg-primary-100 dark:bg-primary-900/20 text-primary-800 dark:text-primary-400">
                      {selectedTopic.category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </span>
                    <span className="px-3 py-1 rounded-full text-sm font-medium bg-secondary-100 dark:bg-secondary-900/20 text-secondary-800 dark:text-secondary-400">
                      {selectedTopic.estimated_read_time}
                    </span>
                  </div>
                </div>
                <div className="flex items-center space-x-2 ml-4">
                  <Button
                    onClick={() => copyToClipboard(selectedTopic.title, 'Title')}
                    variant="ghost"
                    size="sm"
                    className="p-2"
                    title="Copy Title"
                  >
                    <ClipboardDocumentIcon className="h-5 w-5" />
                  </Button>
                  <Button
                    onClick={() => copyToClipboard(selectedTopic.description, 'Description')}
                    variant="ghost"
                    size="sm"
                    className="p-2"
                    title="Copy Description"
                  >
                    <ShareIcon className="h-5 w-5" />
                  </Button>
                  <Button
                    onClick={() => setSelectedTopic(null)}
                    variant="ghost"
                    size="sm"
                    className="p-2"
                  >
                    <XMarkIcon className="h-6 w-6" />
                  </Button>
                </div>
              </div>
            </div>

            {/* Content */}
            <div className="overflow-y-auto max-h-[calc(95vh-140px)] px-8 py-6 bg-gray-50 dark:bg-gray-900">
              {/* Description */}
              <div className="mb-8 animate-fade-in-up">
                <Card variant="gradient" className="border-primary-200 dark:border-primary-700">
                  <CardContent className="p-6">
                    <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-3 flex items-center">
                      <DocumentTextIcon className="h-5 w-5 mr-2 text-primary-600 dark:text-primary-400" />
                      Description
                    </h3>
                    <p className="text-gray-700 dark:text-gray-300 text-lg leading-relaxed">
                      {selectedTopic.description}
                    </p>
                  </CardContent>
                </Card>
              </div>

              {/* Main Content Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                {/* Company & Technologies */}
                <Card className="bg-gradient-to-r from-success-50 to-emerald-50 dark:from-success-900/20 dark:to-emerald-900/20 border-success-200 dark:border-success-700 animate-fade-in-up animation-delay-100">
                  <CardContent className="p-6">
                    <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center">
                      <BuildingOfficeIcon className="h-5 w-5 mr-2 text-success-600 dark:text-success-400" />
                      Company & Technologies
                    </h3>
                    <div className="space-y-4">
                      <div>
                        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Company:</span>
                        <p className="text-gray-800 dark:text-gray-200 font-semibold capitalize">{selectedTopic.company}</p>
                      </div>
                      <div>
                        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Technologies:</span>
                        <div className="flex flex-wrap gap-2 mt-2">
                          {selectedTopic.technologies.map((tech, i) => (
                            <span key={i} className="px-3 py-1 bg-white/70 dark:bg-gray-800/70 rounded-full text-sm font-medium text-gray-700 dark:text-gray-300 border border-success-200 dark:border-success-700">
                              {tech}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Learning Objectives */}
                <Card className="bg-gradient-to-r from-secondary-50 to-pink-50 dark:from-secondary-900/20 dark:to-pink-900/20 border-secondary-200 dark:border-secondary-700 animate-fade-in-up animation-delay-200">
                  <CardContent className="p-6">
                    <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center">
                      <AcademicCapIcon className="h-5 w-5 mr-2 text-secondary-600 dark:text-secondary-400" />
                      Learning Objectives
                    </h3>
                    <ul className="space-y-3">
                      {selectedTopic.learning_objectives.map((obj, i) => (
                        <li key={i} className="flex items-start">
                          <CheckCircleIcon className="h-5 w-5 text-success-500 dark:text-success-400 mr-3 mt-0.5 flex-shrink-0" />
                          <span className="text-gray-700 dark:text-gray-300">{obj}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </div>

              {/* Tags & Prerequisites */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                {/* Tags */}
                <Card className="bg-gradient-to-r from-orange-50 to-red-50 dark:from-orange-900/20 dark:to-red-900/20 border-orange-200 dark:border-orange-700 animate-fade-in-up animation-delay-300">
                  <CardContent className="p-6">
                    <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center">
                      <TagIcon className="h-5 w-5 mr-2 text-orange-600 dark:text-orange-400" />
                      Tags
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {selectedTopic.tags.map((tag, i) => (
                        <span key={i} className="px-3 py-1 bg-white/70 dark:bg-gray-800/70 rounded-full text-sm font-medium text-gray-700 dark:text-gray-300 border border-orange-200 dark:border-orange-700">
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Prerequisites */}
                <Card className="bg-gradient-to-r from-indigo-50 to-blue-50 dark:from-indigo-900/20 dark:to-blue-900/20 border-indigo-200 dark:border-indigo-700 animate-fade-in-up animation-delay-400">
                  <CardContent className="p-6">
                    <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center">
                      <ClockIcon className="h-5 w-5 mr-2 text-indigo-600 dark:text-indigo-400" />
                      Prerequisites
                    </h3>
                    <ul className="space-y-2">
                      {selectedTopic.prerequisites.map((prereq, i) => (
                        <li key={i} className="flex items-start">
                          <StarIcon className="h-4 w-4 text-warning-500 dark:text-warning-400 mr-3 mt-1 flex-shrink-0" />
                          <span className="text-gray-700 dark:text-gray-300">{prereq}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </div>

              {/* Metrics */}
              <Card className="bg-gradient-to-r from-teal-50 to-cyan-50 dark:from-teal-900/20 dark:to-cyan-900/20 border-teal-200 dark:border-teal-700 mb-8 animate-fade-in-up animation-delay-500">
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center">
                    <ChartBarIcon className="h-5 w-5 mr-2 text-teal-600 dark:text-teal-400" />
                    System Metrics
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-white/70 dark:bg-gray-800/70 rounded-xl p-4 border border-teal-200 dark:border-teal-700">
                      <div className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">Scale</div>
                      <div className="text-gray-800 dark:text-gray-200 font-semibold">{selectedTopic.metrics.scale}</div>
                    </div>
                    <div className="bg-white/70 dark:bg-gray-800/70 rounded-xl p-4 border border-teal-200 dark:border-teal-700">
                      <div className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">Performance</div>
                      <div className="text-gray-800 dark:text-gray-200 font-semibold">{selectedTopic.metrics.performance}</div>
                    </div>
                    <div className="bg-white/70 dark:bg-gray-800/70 rounded-xl p-4 border border-teal-200 dark:border-teal-700">
                      <div className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">Reliability</div>
                      <div className="text-gray-800 dark:text-gray-200 font-semibold">{selectedTopic.metrics.reliability}</div>
                    </div>
                    <div className="bg-white/70 dark:bg-gray-800/70 rounded-xl p-4 border border-teal-200 dark:border-teal-700">
                      <div className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">Latency</div>
                      <div className="text-gray-800 dark:text-gray-200 font-semibold">{selectedTopic.metrics.latency}</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Implementation Details */}
              <Card className="bg-gradient-to-r from-gray-50 to-slate-50 dark:from-gray-800/50 dark:to-slate-800/50 border-gray-200 dark:border-gray-700 mb-8 animate-fade-in-up animation-delay-600">
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center">
                    <CogIcon className="h-5 w-5 mr-2 text-gray-600 dark:text-gray-400" />
                    Implementation Details
                  </h3>
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <div>
                        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Architecture:</span>
                        <p className="text-gray-800 dark:text-gray-200 mt-1">{selectedTopic.implementation_details.architecture}</p>
                      </div>
                      <div>
                        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Scaling:</span>
                        <p className="text-gray-800 dark:text-gray-200 mt-1">{selectedTopic.implementation_details.scaling}</p>
                      </div>
                      <div>
                        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Storage:</span>
                        <p className="text-gray-800 dark:text-gray-200 mt-1">{selectedTopic.implementation_details.storage}</p>
                      </div>
                    </div>
                    <div className="space-y-4">
                      <div>
                        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Caching:</span>
                        <p className="text-gray-800 dark:text-gray-200 mt-1">{selectedTopic.implementation_details.caching}</p>
                      </div>
                      <div>
                        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Monitoring:</span>
                        <p className="text-gray-800 dark:text-gray-200 mt-1">{selectedTopic.implementation_details.monitoring}</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Related Topics */}
              {selectedTopic.related_topics && selectedTopic.related_topics.length > 0 && (
                <Card className="bg-gradient-to-r from-violet-50 to-purple-50 dark:from-violet-900/20 dark:to-purple-900/20 border-violet-200 dark:border-violet-700 mb-8 animate-fade-in-up animation-delay-700">
                  <CardContent className="p-6">
                    <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center">
                      <LinkIcon className="h-5 w-5 mr-2 text-violet-600 dark:text-violet-400" />
                      Related Topics
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {selectedTopic.related_topics.map((topicId, i) => (
                        <span key={i} className="px-3 py-1 bg-white/70 dark:bg-gray-800/70 rounded-full text-sm font-medium text-gray-700 dark:text-gray-300 border border-violet-200 dark:border-violet-700">
                          Topic #{topicId}
                        </span>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Action Buttons */}
              <Card className="bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20 border-primary-200 dark:border-primary-700 mb-6 animate-fade-in-up animation-delay-800">
                <CardContent className="p-6">
                  <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                    <Button
                      onClick={() => {
                        const contentGeneratorUrl = `/content-generator?topicId=${selectedTopic.id}`;
                        window.open(contentGeneratorUrl, '_blank');
                      }}
                      variant="primary"
                      size="lg"
                      className="shadow-lg hover:shadow-xl"
                    >
                      <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                      Generate Content
                    </Button>
                    <div className="text-sm text-gray-600 dark:text-gray-400 text-center">
                      Create multi-platform content for this topic
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Footer */}
              <Card className="bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800/50 dark:to-gray-700/50 border-gray-200 dark:border-gray-700 animate-fade-in-up animation-delay-900">
                <CardContent className="p-6">
                  <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center text-sm text-gray-600 dark:text-gray-400">
                    <div className="space-y-1">
                      <div><span className="font-medium">Created:</span> {selectedTopic.created_date}</div>
                      <div><span className="font-medium">Updated:</span> {selectedTopic.updated_date}</div>
                    </div>
                    <div className="mt-4 sm:mt-0">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusBadgeClass('completed')}`}>
                        Status: completed
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Topics;