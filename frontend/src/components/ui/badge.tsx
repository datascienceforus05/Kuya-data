import * as React from "react";
import { cn } from "@/lib/utils";

const Badge = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement> & {
        variant?: "default" | "secondary" | "destructive" | "outline" | "success" | "pro";
    }
>(({ className, variant = "default", ...props }, ref) => {
    const variants = {
        default:
            "bg-gradient-to-r from-purple-600 to-indigo-600 text-white",
        secondary:
            "bg-secondary text-secondary-foreground",
        destructive:
            "bg-destructive text-destructive-foreground",
        outline:
            "border border-input bg-background text-foreground",
        success:
            "bg-gradient-to-r from-emerald-500 to-teal-500 text-white",
        pro:
            "bg-gradient-to-r from-amber-500 via-orange-500 to-yellow-500 text-white",
    };

    return (
        <div
            ref={ref}
            className={cn(
                "inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold transition-colors",
                variants[variant],
                className
            )}
            {...props}
        />
    );
});
Badge.displayName = "Badge";

export { Badge };
