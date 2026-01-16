"use client";

import React, { useRef } from "react";
import { usePathname } from "next/navigation";
import { motion, useInView, Variants } from "framer-motion";
import { Sparkles, Zap, Star } from "lucide-react";

export function Footer() {
    const pathname = usePathname();
    const containerRef = useRef(null);
    const isInView = useInView(containerRef, {
        once: false,
        amount: 0.3,
        margin: "-100px"
    });

    // Do not show footer on admin pages
    if (pathname?.startsWith("/admin")) return null;

    const kuyaLetters = ["K", "u", "y", "a"];

    // Animation variants for letters
    const letterVariants: Variants = {
        hidden: {
            opacity: 0,
            y: 150,
            scale: 0.8
        },
        visible: (i: number) => ({
            opacity: 1,
            y: 0,
            scale: 1,
            transition: {
                delay: i * 0.15,
                duration: 0.8,
                type: "spring",
                stiffness: 100,
                damping: 12
            }
        })
    };

    const textVariants = {
        hidden: { opacity: 0, y: 30 },
        visible: {
            opacity: 1,
            y: 0,
            transition: { duration: 0.6 }
        }
    };

    return (
        <footer className="relative overflow-hidden bg-gradient-to-b from-purple-50 via-indigo-50 to-white dark:from-gray-900 dark:via-purple-900/10 dark:to-gray-950">
            {/* Decorative Elements */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                {/* Floating Orbs */}
                <motion.div
                    animate={{
                        y: [0, -30, 0],
                        opacity: [0.2, 0.5, 0.2]
                    }}
                    transition={{ duration: 5, repeat: Infinity }}
                    className="absolute top-10 left-[8%] w-40 h-40 bg-purple-400/20 rounded-full blur-3xl"
                />
                <motion.div
                    animate={{
                        y: [0, 25, 0],
                        opacity: [0.15, 0.4, 0.15]
                    }}
                    transition={{ duration: 6, repeat: Infinity }}
                    className="absolute top-1/3 right-[10%] w-56 h-56 bg-indigo-400/20 rounded-full blur-3xl"
                />
                <motion.div
                    animate={{
                        y: [0, -20, 0],
                        opacity: [0.3, 0.6, 0.3]
                    }}
                    transition={{ duration: 4, repeat: Infinity }}
                    className="absolute bottom-1/4 left-[20%] w-32 h-32 bg-pink-400/20 rounded-full blur-2xl"
                />
                <motion.div
                    animate={{
                        scale: [1, 1.2, 1],
                        opacity: [0.2, 0.4, 0.2]
                    }}
                    transition={{ duration: 7, repeat: Infinity }}
                    className="absolute top-1/2 right-[25%] w-48 h-48 bg-cyan-400/10 rounded-full blur-3xl"
                />

                {/* Sparkle Elements */}
                <motion.div
                    animate={{ rotate: 360, scale: [1, 1.2, 1] }}
                    transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                    className="absolute top-20 right-[18%] text-purple-300/60"
                >
                    <Sparkles className="w-10 h-10" />
                </motion.div>
                <motion.div
                    animate={{ rotate: -360 }}
                    transition={{ duration: 12, repeat: Infinity, ease: "linear" }}
                    className="absolute top-1/3 left-[12%] text-indigo-300/50"
                >
                    <Star className="w-8 h-8" />
                </motion.div>
                <motion.div
                    animate={{ scale: [1, 1.3, 1], opacity: [0.4, 0.8, 0.4] }}
                    transition={{ duration: 2.5, repeat: Infinity }}
                    className="absolute top-16 left-[30%] text-purple-400/40"
                >
                    <Zap className="w-12 h-12" />
                </motion.div>
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
                    className="absolute bottom-1/3 right-[8%] text-pink-300/40"
                >
                    <Sparkles className="w-6 h-6" />
                </motion.div>

                {/* Decorative Dots */}
                <div className="absolute top-1/4 left-[5%] w-2 h-2 bg-purple-400/30 rounded-full" />
                <div className="absolute top-1/3 right-[12%] w-3 h-3 bg-indigo-400/30 rounded-full" />
                <div className="absolute bottom-1/4 left-[15%] w-2 h-2 bg-pink-400/30 rounded-full" />
                <div className="absolute top-1/2 right-[5%] w-4 h-4 bg-purple-400/20 rounded-full" />
            </div>

            <div ref={containerRef} className="section-container relative z-10 pt-16 pb-0">
                {/* Top Text */}
                <motion.p
                    variants={textVariants}
                    initial="hidden"
                    animate={isInView ? "visible" : "hidden"}
                    className="text-center text-lg md:text-xl lg:text-2xl text-gray-500 dark:text-gray-400 font-medium mb-4"
                >
                    Transform your data with
                </motion.p>

                {/* Giant Animated KUYA Text - Coming from bottom */}
                <div className="flex justify-center items-end overflow-hidden" style={{ marginBottom: "-0.15em", minHeight: "20rem" }}>
                    {kuyaLetters.map((letter, idx) => (
                        <motion.span
                            key={idx}
                            custom={idx}
                            variants={letterVariants}
                            initial="hidden"
                            animate={isInView ? "visible" : "hidden"}
                            className="text-[10rem] md:text-[16rem] lg:text-[22rem] xl:text-[28rem] font-display font-black leading-[0.75] select-none inline-block"
                            style={{
                                background: "linear-gradient(160deg, #9333ea 0%, #6366f1 40%, #ec4899 100%)",
                                WebkitBackgroundClip: "text",
                                WebkitTextFillColor: "transparent",
                                backgroundClip: "text",
                                filter: "drop-shadow(0 30px 60px rgba(139, 92, 246, 0.25))"
                            }}
                        >
                            {letter}
                        </motion.span>
                    ))}
                </div>
            </div>
        </footer>
    );
}
