import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'danger' | 'warning' | 'secondary';
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({ variant = 'primary', children, className = '', ...props }) => {
  const base = "px-4 py-2 rounded-lg font-medium transition-colors shadow-sm focus:outline-none";
  const variants = {
    primary: "bg-emerald-600 hover:bg-emerald-700 text-white",
    danger: "bg-red-600 hover:bg-red-700 text-white",
    warning: "bg-amber-500 hover:bg-amber-600 text-white",
    secondary: "bg-slate-200 hover:bg-slate-300 text-slate-800"
  };
  return <button className={`${base} ${variants[variant]} ${className}`} {...props}>{children}</button>;
};
