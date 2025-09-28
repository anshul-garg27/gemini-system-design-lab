// JavaScript for System Design Topic Generator

class TopicGenerator {
    constructor() {
        this.socket = io();
        this.isProcessing = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupSocketListeners();
        this.loadRecentTopics();
    }

    setupEventListeners() {
        // Form submission
        document.getElementById('bulkTopicForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitTopics();
        });

        // Clear form
        document.getElementById('clearForm').addEventListener('click', () => {
            this.clearForm();
        });

        // Real-time character count
        document.getElementById('topicTitles').addEventListener('input', (e) => {
            this.updateCharacterCount(e.target.value);
        });
    }

    setupSocketListeners() {
        this.socket.on('status_update', (status) => {
            this.updateProcessingStatus(status);
        });

        this.socket.on('connect', () => {
            console.log('Connected to server');
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });
    }

    async submitTopics() {
        const topicTitles = document.getElementById('topicTitles').value.trim();
        const batchSize = parseInt(document.getElementById('batchSize').value);

        if (!topicTitles) {
            this.showToast('Please enter at least one topic title', 'warning');
            return;
        }

        const topics = topicTitles.split('\n').filter(title => title.trim());
        
        if (topics.length === 0) {
            this.showToast('Please enter valid topic titles', 'warning');
            return;
        }

        try {
            this.setProcessingState(true);
            
            const response = await fetch('/api/topics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    topics: topics,
                    batch_size: batchSize
                })
            });

            const result = await response.json();

            if (response.ok) {
                this.showToast(`Started processing ${result.total_topics} topics`, 'success');
                this.showProcessingSection();
            } else {
                this.showToast(result.error || 'Failed to start processing', 'danger');
                this.setProcessingState(false);
            }
        } catch (error) {
            console.error('Error submitting topics:', error);
            this.showToast('Network error occurred', 'danger');
            this.setProcessingState(false);
        }
    }

    updateProcessingStatus(status) {
        if (status.is_processing) {
            this.showProcessingSection();
            this.updateProgress(status);
        } else {
            this.hideProcessingSection();
            this.setProcessingState(false);
            
            if (status.processed_topics > 0) {
                this.showToast(`Processing complete! ${status.processed_topics} topics generated`, 'success');
                this.loadRecentTopics();
            }
        }

        // Update current status
        if (status.current_topic) {
            document.getElementById('currentStatus').textContent = status.current_topic;
        }

        // Update batch progress
        if (status.total_batches > 0) {
            document.getElementById('batchProgress').textContent = 
                `${status.current_batch} / ${status.total_batches}`;
        }

        // Update counts
        document.getElementById('processedCount').textContent = status.processed_topics || 0;
        document.getElementById('failedCount').textContent = status.failed_topics || 0;

        // Show errors if any
        if (status.errors && status.errors.length > 0) {
            status.errors.forEach(error => {
                this.showToast(error, 'danger');
            });
        }
    }

    updateProgress(status) {
        if (status.total_batches > 0) {
            const progress = (status.current_batch / status.total_batches) * 100;
            const progressBar = document.getElementById('progressBar');
            const progressText = document.getElementById('progressText');
            
            progressBar.style.width = `${progress}%`;
            progressText.textContent = `${Math.round(progress)}%`;
        }
    }

    showProcessingSection() {
        document.getElementById('processingSection').style.display = 'block';
        document.getElementById('processingSection').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
    }

    hideProcessingSection() {
        setTimeout(() => {
            document.getElementById('processingSection').style.display = 'none';
        }, 3000);
    }

    setProcessingState(processing) {
        this.isProcessing = processing;
        const submitBtn = document.getElementById('submitBtn');
        const form = document.getElementById('bulkTopicForm');
        
        if (processing) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            form.classList.add('loading');
        } else {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-play me-2"></i>Generate Topics';
            form.classList.remove('loading');
        }
    }

    clearForm() {
        document.getElementById('topicTitles').value = '';
        document.getElementById('batchSize').value = '3';
        this.updateCharacterCount('');
    }

    updateCharacterCount(text) {
        const lines = text.split('\n').filter(line => line.trim());
        const charCount = text.length;
        
        // You can add character count display here if needed
        console.log(`Lines: ${lines.length}, Characters: ${charCount}`);
    }

    async loadRecentTopics() {
        try {
            const response = await fetch('/api/topics?limit=5');
            const topics = await response.json();
            
            this.displayRecentTopics(topics);
        } catch (error) {
            console.error('Error loading recent topics:', error);
        }
    }

    displayRecentTopics(topics) {
        const tbody = document.getElementById('recentTopicsTable');
        
        if (topics.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center text-muted py-4">
                        <i class="fas fa-inbox me-2"></i>No topics found
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = topics.map(topic => `
            <tr>
                <td><span class="badge bg-primary">${topic.id}</span></td>
                <td>
                    <div class="fw-semibold">${this.escapeHtml(topic.title)}</div>
                    <small class="text-muted">${this.escapeHtml(topic.description.substring(0, 100))}...</small>
                </td>
                <td>
                    <span class="badge bg-info">${topic.category}</span>
                </td>
                <td>
                    <span class="fw-semibold text-capitalize">${topic.company}</span>
                </td>
                <td>
                    <span class="badge ${this.getComplexityBadgeClass(topic.complexity_level)}">
                        ${topic.complexity_level}
                    </span>
                    <small class="d-block text-muted">${topic.difficulty}/10</small>
                </td>
                <td>
                    <span class="badge ${this.getStatusBadgeClass(topic.processing_status || 'completed')}">
                        ${topic.processing_status || 'completed'}
                    </span>
                </td>
                <td>
                    <div class="btn-group" role="group">
                        <button class="btn btn-sm btn-outline-primary" onclick="topicGenerator.viewTopic(${topic.id})">
                            <i class="fas fa-eye"></i>
                        </button>
                        ${topic.processing_status === 'failed' ? `
                            <button class="btn btn-sm btn-outline-warning" onclick="topicGenerator.retryTopic(${topic.id})">
                                <i class="fas fa-redo"></i>
                            </button>
                        ` : ''}
                    </div>
                </td>
            </tr>
        `).join('');
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

    getStatusBadgeClass(status) {
        const classes = {
            'completed': 'bg-success',
            'pending': 'bg-warning',
            'failed': 'bg-danger'
        };
        return classes[status] || 'bg-secondary';
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
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-file-alt me-2"></i>${this.escapeHtml(topic.title)}
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <strong>Category:</strong> 
                                    <span class="badge bg-info">${topic.category}</span>
                                </div>
                                <div class="col-md-6">
                                    <strong>Company:</strong> 
                                    <span class="fw-semibold text-capitalize">${topic.company}</span>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <strong>Complexity:</strong> 
                                    <span class="badge ${this.getComplexityBadgeClass(topic.complexity_level)}">
                                        ${topic.complexity_level}
                                    </span>
                                    <small class="text-muted">(${topic.difficulty}/10)</small>
                                </div>
                                <div class="col-md-6">
                                    <strong>Read Time:</strong> 
                                    <span class="fw-semibold">${topic.estimated_read_time}</span>
                                </div>
                            </div>
                            <div class="mb-3">
                                <strong>Description:</strong>
                                <p class="mt-2">${this.escapeHtml(topic.description)}</p>
                            </div>
                            <div class="mb-3">
                                <strong>Technologies:</strong>
                                <div class="mt-2">
                                    ${topic.technologies.map(tech => 
                                        `<span class="badge bg-secondary me-1">${this.escapeHtml(tech)}</span>`
                                    ).join('')}
                                </div>
                            </div>
                            <div class="mb-3">
                                <strong>Learning Objectives:</strong>
                                <ul class="mt-2">
                                    ${topic.learning_objectives.map(obj => 
                                        `<li>${this.escapeHtml(obj)}</li>`
                                    ).join('')}
                                </ul>
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
        try {
            const response = await fetch(`/api/topics/${topicId}/retry`, {
                method: 'POST'
            });

            const result = await response.json();

            if (response.ok) {
                this.showToast('Topic retry initiated', 'success');
                this.loadRecentTopics();
            } else {
                this.showToast(result.error || 'Failed to retry topic', 'danger');
            }
        } catch (error) {
            console.error('Error retrying topic:', error);
            this.showToast('Network error occurred', 'danger');
        }
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

// Initialize the application
const topicGenerator = new TopicGenerator();

// Add some utility functions
window.topicGenerator = topicGenerator;
