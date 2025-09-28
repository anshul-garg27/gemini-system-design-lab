// JavaScript for Analytics page

class AnalyticsDashboard {
    constructor() {
        this.init();
    }

    init() {
        this.setupCharts();
    }

    setupCharts() {
        // Category Chart
        this.setupCategoryChart();
        
        // Complexity Chart
        this.setupComplexityChart();
        
        // Daily Activity Chart
        this.setupDailyChart();
    }

    setupCategoryChart() {
        const ctx = document.getElementById('categoryChart').getContext('2d');
        const categoryData = {{ (stats.category_breakdown or {}) | tojson }};
        
        const labels = Object.keys(categoryData).map(key => 
            key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
        );
        const data = Object.values(categoryData);
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        '#6366f1', '#10b981', '#f59e0b', '#ef4444', '#06b6d4',
                        '#8b5cf6', '#f97316', '#84cc16', '#ec4899', '#6b7280'
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                            }
                        }
                    }
                }
            }
        });
    }

    setupComplexityChart() {
        const ctx = document.getElementById('complexityChart').getContext('2d');
        const complexityData = {{ (stats.complexity_breakdown or {}) | tojson }};
        
        const labels = Object.keys(complexityData).map(key => 
            key.charAt(0).toUpperCase() + key.slice(1)
        );
        const data = Object.values(complexityData);
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Topics',
                    data: data,
                    backgroundColor: [
                        '#10b981', // beginner - green
                        '#f59e0b', // intermediate - yellow
                        '#ef4444', // advanced - red
                        '#1f2937'  // expert - dark
                    ],
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#6366f1',
                        borderWidth: 1
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        ticks: {
                            stepSize: 1
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    setupDailyChart() {
        const ctx = document.getElementById('dailyChart').getContext('2d');
        const dailyData = {{ (stats.daily_stats or []) | tojson }};
        
        // Process daily data
        const labels = dailyData.map(item => {
            const date = new Date(item[0]);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        }).reverse();
        
        const data = dailyData.map(item => item[1]).reverse();
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Topics Generated',
                    data: data,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#6366f1',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#6366f1',
                        borderWidth: 1,
                        callbacks: {
                            title: function(context) {
                                const date = new Date(dailyData[dailyData.length - 1 - context[0].dataIndex][0]);
                                return date.toLocaleDateString('en-US', { 
                                    weekday: 'long', 
                                    year: 'numeric', 
                                    month: 'long', 
                                    day: 'numeric' 
                                });
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        ticks: {
                            stepSize: 1
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
    }
}

// Initialize the analytics dashboard
const analyticsDashboard = new AnalyticsDashboard();
