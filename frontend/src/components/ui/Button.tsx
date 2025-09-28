import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../../lib/utils';

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none",
  {
    variants: {
      variant: {
        primary: "bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white shadow-md hover:shadow-lg focus:ring-primary-500",
        secondary: "bg-gray-100 hover:bg-gray-200 text-gray-900 border border-gray-300 focus:ring-gray-500",
        success: "bg-gradient-to-r from-success-500 to-success-600 hover:from-success-600 hover:to-success-700 text-white shadow-md hover:shadow-lg focus:ring-success-500",
        warning: "bg-gradient-to-r from-warning-500 to-warning-600 hover:from-warning-600 hover:to-warning-700 text-white shadow-md hover:shadow-lg focus:ring-warning-500",
        error: "bg-gradient-to-r from-error-500 to-error-600 hover:from-error-600 hover:to-error-700 text-white shadow-md hover:shadow-lg focus:ring-error-500",
        ghost: "hover:bg-gray-100 text-gray-700 focus:ring-gray-500",
        outline: "border border-primary-500 text-primary-600 hover:bg-primary-50 focus:ring-primary-500",
        link: "text-primary-600 hover:text-primary-700 underline-offset-4 hover:underline focus:ring-primary-500",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base",
        xl: "h-14 px-8 text-lg",
        icon: "h-10 w-10",
      },
      animation: {
        none: "",
        bounce: "hover:animate-bounce-subtle",
        pulse: "hover:animate-pulse",
        glow: "hover:animate-glow",
      }
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
      animation: "none",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, animation, loading, leftIcon, rightIcon, children, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, animation, className }))}
        ref={ref}
        disabled={loading}
        {...props}
      >
        {loading && (
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        )}
        {!loading && leftIcon && <span className="mr-2">{leftIcon}</span>}
        {children}
        {!loading && rightIcon && <span className="ml-2">{rightIcon}</span>}
      </button>
    );
  }
);

Button.displayName = "Button";

export { Button, buttonVariants };
