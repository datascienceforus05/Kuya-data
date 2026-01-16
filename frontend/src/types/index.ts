export interface User {
    id: string;
    name: string;
    email: string;
    image?: string;
    plan: "free" | "pro";
    createdAt: string;
}

export interface Report {
    _id: string;
    reportId: string;
    userEmail: string;
    fileName: string;
    createdAt: string;
    summary: DataSummary;
    correlation: Record<string, Record<string, number>>;
    graphs: GraphData[];
}

export interface DataSummary {
    rows: number;
    columns: number;
    numericColumns: string[];
    categoricalColumns: string[];
    missingValues: Record<string, number>;
    statistics: Record<string, ColumnStats>;
}

export interface ColumnStats {
    count: number;
    mean?: number;
    std?: number;
    min?: number;
    max?: number;
    unique?: number;
    top?: string;
    freq?: number;
}

export interface GraphData {
    type: "missing_values" | "correlation" | "distribution" | "histogram";
    title: string;
    image: string; // base64 encoded
}

export interface UploadResponse {
    success: boolean;
    reportId: string;
    summary: DataSummary;
    correlation: Record<string, Record<string, number>>;
    graphs: GraphData[];
    cleanedDataHead: Record<string, unknown>[];
    insights: string[];
}

export interface ApiError {
    message: string;
    code?: string;
}
