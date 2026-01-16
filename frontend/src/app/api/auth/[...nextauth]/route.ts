import NextAuth, { NextAuthOptions } from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import { MongoDBAdapter } from "@auth/mongodb-adapter";
import clientPromise from "@/lib/mongodb";

export const authOptions: NextAuthOptions = {
    adapter: MongoDBAdapter(clientPromise) as any,
    providers: [
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID!,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
        }),
    ],
    pages: {
        signIn: "/login",
        error: "/login",
    },
    callbacks: {
        async session({ session, user }) {
            if (session.user) {
                session.user.id = user.id;
                // Fetch user plan from database
                try {
                    const response = await fetch(
                        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/user/${encodeURIComponent(session.user.email!)}`
                    );
                    if (response.ok) {
                        const userData = await response.json();
                        (session.user as any).plan = userData.plan || "free";
                    }
                } catch (error) {
                    console.error("Failed to fetch user plan:", error);
                    (session.user as any).plan = "free";
                }
            }
            return session;
        },
        async signIn({ user, account }) {
            if (user.email) {
                // Create/update user in backend
                try {
                    await fetch(
                        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/auth/register`,
                        {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({
                                name: user.name,
                                email: user.email,
                                image: user.image,
                            }),
                        }
                    );
                } catch (error) {
                    console.error("Failed to register user:", error);
                }
            }
            return true;
        },
        async redirect({ url, baseUrl }: { url: string; baseUrl: string }) {
            // Allow all internal routes
            if (url.startsWith("/")) return `${baseUrl}${url}`;
            // Allow only same domain redirects
            else if (url.startsWith(baseUrl)) return url;
            return baseUrl;
        },
    },
    session: {
        strategy: "database",
    },
    secret: process.env.NEXTAUTH_SECRET,
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
