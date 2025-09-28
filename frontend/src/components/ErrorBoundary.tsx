import React from 'react';

type ErrorBoundaryState = { hasError: boolean; error?: any };

type ErrorBoundaryProps = { children: React.ReactNode };

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: any) {
    return { hasError: true, error };
  }

  componentDidCatch(error: any, info: any) {
    // Optionally log to monitoring
    console.error('ErrorBoundary caught an error', error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full p-6">
          <div className="text-center text-red-600">
            <h2 className="text-xl font-bold mb-2">Something went wrong.</h2>
            <p className="text-sm text-gray-600">Please close and reopen the view. If the issue persists, check the content JSON shape.</p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
