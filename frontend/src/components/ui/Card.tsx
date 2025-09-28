import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../../lib/utils';

const cardVariants = cva(
  "rounded-xl border transition-all duration-200",
  {
    variants: {
      variant: {
        default: "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md dark:shadow-gray-900/50 dark:hover:shadow-xl",
        elevated: "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 shadow-md hover:shadow-lg dark:shadow-gray-900/50",
        outlined: "bg-transparent border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500",
        filled: "bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800",
        glass: "bg-white/10 dark:bg-gray-800/10 backdrop-blur-sm border-white/20 dark:border-gray-700/20 shadow-lg",
        gradient: "bg-gradient-to-br from-white to-gray-50 dark:from-gray-800 dark:to-gray-900 border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md",
      },
      padding: {
        none: "p-0",
        sm: "p-4",
        md: "p-6",
        lg: "p-8",
        xl: "p-10",
      },
      hover: {
        none: "",
        lift: "hover:-translate-y-1",
        scale: "hover:scale-105",
        glow: "hover:shadow-glow",
      }
    },
    defaultVariants: {
      variant: "default",
      padding: "md",
      hover: "none",
    },
  }
);

export interface CardProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof cardVariants> {
  asChild?: boolean;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant, padding, hover, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(cardVariants({ variant, padding, hover, className }))}
      {...props}
    />
  )
);

Card.displayName = "Card";

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col space-y-1.5 pb-4", className)} {...props} />
  )
);

CardHeader.displayName = "CardHeader";

const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn("text-lg font-semibold leading-none tracking-tight", className)}
      {...props}
    />
  )
);

CardTitle.displayName = "CardTitle";

const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn("text-sm text-gray-600", className)} {...props} />
  )
);

CardDescription.displayName = "CardDescription";

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("pt-0", className)} {...props} />
  )
);

CardContent.displayName = "CardContent";

const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex items-center pt-4", className)} {...props} />
  )
);

CardFooter.displayName = "CardFooter";

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent };
