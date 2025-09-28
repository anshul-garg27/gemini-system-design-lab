// JavaScript for Topics page

class TopicsManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFilters();
    }

    setupEventListeners() {
        // Select all checkbox
        document.getElementById('selectAll').addEventListener('change', (e) => {
            const checkboxes = document.querySelectorAll('.topic-checkbox');
            checkboxes.forEach(checkbox => {
                checkbox.checked = e.target.checked;
            });
        });

        // Individual checkboxes
        document.querySelectorAll('.topic-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.updateSelectAllState();
            });
        });
    }

    setupFilters() {
        const filters = ['categoryFilter', 'complexityFilter', 'statusFilter', 'searchInput'];
        
        filters.forEach(filterId => {
            const element = document.getElementById(filterId);
            if (element) {
                element.addEventListener('change', () => {
                    this.applyFilters();
                });
            }
        });
    }

    updateSelectAllState() {
        const checkboxes = document.querySelectorAll('.topic-checkbox');
        const checkedBoxes = document.querySelectorAll('.topic-checkbox:checked');
        const selectAllCheckbox = document.getElementById('selectAll');
        
        selectAllCheckbox.checked = checkboxes.length === checkedBoxes.length;
        selectAllCheckbox.indeterminate = checkedBoxes.length > 0 && checkedBoxes.length < checkboxes.length;
    }

    applyFilters() {
        const categoryFilter = document.getElementById('categoryFilter').value;
        const complexityFilter = document.getElementById('complexityFilter').value;
        const statusFilter = document.getElementById('statusFilter').value;
        const searchInput = document.getElementById('searchInput').value.toLowerCase();

        const rows = document.querySelectorAll('#topicsTableBody tr');
        let visibleCount = 0;

        rows.forEach(row => {
            const category = row.dataset.category;
            const complexity = row.dataset.complexity;
            const status = row.dataset.status;
            const title = row.querySelector('td:nth-child(3) .fw-semibold').textContent.toLowerCase();
            const description = row.querySelector('td:nth-child(3) small').textContent.toLowerCase();

            const categoryMatch = !categoryFilter || category === categoryFilter;
            const complexityMatch = !complexityFilter || complexity === complexityFilter;
            const statusMatch = !statusFilter || status === statusFilter;
            const searchMatch = !searchInput || title.includes(searchInput) || description.includes(searchInput);

            if (categoryMatch && complexityMatch && statusMatch && searchMatch) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });

        // Update topics count
        document.getElementById('topicsCount').textContent = visibleCount;
    }

    async viewTopic(topicId) {
        try {
            const response = await fetch(`/api/topics/${topicId}`);
            const topic = await response.json();
            
            this.showTopicModal(topic);
        } catch (error) {
            console.error('Error loading topic:', error);
            this.showToast('Error loading topic details', 'danger');
        }
    }

    showTopicModal(topic) {
        const modalHtml = `
            <div class="modal fade" id="topicModal" tabindex="-1">
                <div class="modal-dialog modal-xl">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-file-alt me-2"></i>${this.escapeHtml(topic.title)}
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row mb-4">
                                <div class="col-md-6">
                                    <div class="info-card">
                                        <h6 class="info-label">Category</h6>
                                        <span class="badge bg-info">${topic.category.replace('_', ' ').toUpperCase()}</span>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="info-card">
                                        <h6 class="info-label">Company</h6>
                                        <span class="fw-semibold text-capitalize">${topic.company}</span>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="row mb-4">
                                <div class="col-md-6">
                                    <div class="info-card">
                                        <h6 class="info-label">Complexity</h6>
                                        <span class="badge ${this.getComplexityBadgeClass(topic.complexity_level)}">
                                            ${topic.complexity_level.toUpperCase()}
                                        </span>
                                        <small class="text-muted ms-2">(${topic.difficulty}/10)</small>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="info-card">
                                        <h6 class="info-label">Read Time</h6>
                                        <span class="fw-semibold">${topic.estimated_read_time}</span>
                                    </div>
                                </div>
                            </div>

                            <div class="mb-4">
                                <h6 class="info-label">Description</h6>
                                <p class="mt-2">${this.escapeHtml(topic.description)}</p>
                            </div>

                            <div class="row mb-4">
                                <div class="col-md-6">
                                    <h6 class="info-label">Technologies</h6>
                                    <div class="mt-2">
                                        ${topic.technologies.map(tech => 
                                            `<span class="badge bg-secondary me-1 mb-1">${this.escapeHtml(tech)}</span>`
                                        ).join('')}
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <h6 class="info-label">Tags</h6>
                                    <div class="mt-2">
                                        ${topic.tags.map(tag => 
                                            `<span class="badge bg-light text-dark me-1 mb-1">${this.escapeHtml(tag)}</span>`
                                        ).join('')}
                                    </div>
                                </div>
                            </div>

                            <div class="row mb-4">
                                <div class="col-md-6">
                                    <h6 class="info-label">Metrics</h6>
                                    <div class="metrics-grid">
                                        <div class="metric-item">
                                            <strong>Scale:</strong> ${this.escapeHtml(topic.metrics.scale)}
                                        </div>
                                        <div class="metric-item">
                                            <strong>Performance:</strong> ${this.escapeHtml(topic.metrics.performance)}
                                        </div>
                                        <div class="metric-item">
                                            <strong>Reliability:</strong> ${this.escapeHtml(topic.metrics.reliability)}
                                        </div>
                                        <div class="metric-item">
                                            <strong>Latency:</strong> ${this.escapeHtml(topic.metrics.latency)}
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <h6 class="info-label">Implementation Details</h6>
                                    <div class="implementation-details">
                                        <div class="impl-item">
                                            <strong>Architecture:</strong> ${this.escapeHtml(topic.implementation_details.architecture)}
                                        </div>
                                        <div class="impl-item">
                                            <strong>Scaling:</strong> ${this.escapeHtml(topic.implementation_details.scaling)}
                                        </div>
                                        <div class="impl-item">
                                            <strong>Storage:</strong> ${this.escapeHtml(topic.implementation_details.storage)}
                                        </div>
                                        <div class="impl-item">
                                            <strong>Caching:</strong> ${this.escapeHtml(topic.implementation_details.caching)}
                                        </div>
                                        <div class="impl-item">
                                            <strong>Monitoring:</strong> ${this.escapeHtml(topic.implementation_details.monitoring)}
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="mb-4">
                                <h6 class="info-label">Learning Objectives</h6>
                                <ul class="mt-2">
                                    ${topic.learning_objectives.map(obj => 
                                        `<li>${this.escapeHtml(obj)}</li>`
                                    ).join('')}
                                </ul>
                            </div>

                            <div class="mb-4">
                                <h6 class="info-label">Prerequisites</h6>
                                <div class="mt-2">
                                    ${topic.prerequisites.map(prereq => 
                                        `<span class="badge bg-warning me-1 mb-1">${this.escapeHtml(prereq)}</span>`
                                    ).join('')}
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-6">
                                    <h6 class="info-label">Related Topics</h6>
                                    <div class="mt-2">
                                        ${topic.related_topics.map(id => 
                                            `<span class="badge bg-primary me-1 mb-1">#${id}</span>`
                                        ).join('')}
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <h6 class="info-label">Created</h6>
                                    <p class="mt-2 mb-0">${topic.created_date}</p>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Remove existing modal if any
        const existingModal = document.getElementById('topicModal');
        if (existingModal) {
            existingModal.remove();
        }

        // Add modal to DOM
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('topicModal'));
        modal.show();
    }

    async retryTopic(topicId) {
        if (!confirm('Are you sure you want to retry processing this topic?')) {
            return;
        }

        try {
            const response = await fetch(`/api/topics/${topicId}/retry`, {
                method: 'POST'
            });

            const result = await response.json();

            if (response.ok) {
                this.showToast('Topic retry initiated', 'success');
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            } else {
                this.showToast(result.error || 'Failed to retry topic', 'danger');
            }
        } catch (error) {
            console.error('Error retrying topic:', error);
            this.showToast('Network error occurred', 'danger');
        }
    }

    async deleteTopic(topicId) {
        if (!confirm('Are you sure you want to delete this topic? This action cannot be undone.')) {
            return;
        }

        try {
            const response = await fetch(`/api/topics/${topicId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showToast('Topic deleted successfully', 'success');
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            } else {
                const result = await response.json();
                this.showToast(result.error || 'Failed to delete topic', 'danger');
            }
        } catch (error) {
            console.error('Error deleting topic:', error);
            this.showToast('Network error occurred', 'danger');
        }
    }

    getComplexityBadgeClass(complexity) {
        const classes = {
            'beginner': 'bg-success',
            'intermediate': 'bg-warning',
            'advanced': 'bg-danger',
            'expert': 'bg-dark'
        };
        return classes[complexity] || 'bg-secondary';
    }

    showToast(message, type = 'info') {
        const toastHtml = `
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="fas fa-${this.getToastIcon(type)} me-2"></i>${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;

        // Create toast container if it doesn't exist
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        // Add toast
        container.insertAdjacentHTML('beforeend', toastHtml);
        
        // Show toast
        const toastElement = container.lastElementChild;
        const toast = new bootstrap.Toast(toastElement);
        toast.show();

        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }

    getToastIcon(type) {
        const icons = {
            'success': 'check-circle',
            'danger': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Global functions for onclick handlers
function viewTopic(topicId) {
    topicsManager.viewTopic(topicId);
}

function retryTopic(topicId) {
    topicsManager.retryTopic(topicId);
}

function deleteTopic(topicId) {
    topicsManager.deleteTopic(topicId);
}

function refreshTopics() {
    window.location.reload();
}

function exportTopics() {
    // Implementation for exporting topics
    window.open('/api/export', '_blank');
}

// Initialize the topics manager
const topicsManager = new TopicsManager();
