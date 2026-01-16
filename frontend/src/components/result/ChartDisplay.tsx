"use client";

import React from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface ChartDisplayProps {
    title: string;
    image: string; // base64 encoded
    delay?: number;
}

export function ChartDisplay({ title, image, delay = 0 }: ChartDisplayProps) {
    return (
        <div className="h-full">
            <Card glass className="overflow-hidden hover:shadow-glow transition-all duration-300 h-full">
                <CardHeader className="pb-4">
                    <CardTitle className="text-lg">{title}</CardTitle>
                </CardHeader>
                <CardContent className="p-0">
                    <div className="relative aspect-[4/3] bg-gray-50 dark:bg-gray-800/50">
                        {image ? (
                            <img
                                src={image.startsWith("data:") ? image : `data:image/png;base64,${image}`}
                                alt={title}
                                className="w-full h-full object-contain"
                            />
                        ) : (
                            <div className="absolute inset-0 flex items-center justify-center text-gray-400">
                                Chart not available
                            </div>
                        )}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
