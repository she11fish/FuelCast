import { Calendar } from "lucide-react";
import { cn } from "@/lib/utils";

export type TimeRange = "all" | "last-year" | "forecast";

interface TimeRangeSelectorProps {
  value: TimeRange;
  onChange: (value: TimeRange) => void;
}

export function TimeRangeSelector({ value, onChange }: TimeRangeSelectorProps) {
  const options: { value: TimeRange; label: string }[] = [
    { value: "all", label: "All Time" },
    { value: "last-year", label: "Last Year" },
    { value: "forecast", label: "Forecast Only" },
  ];

  return (
    <div className="flex items-center gap-3 mb-6">
      <div className="flex items-center gap-2 text-muted-foreground">
        <Calendar className="w-4 h-4" />
        <span className="text-sm font-medium">Time Range:</span>
      </div>
      <div className="flex gap-2">
        {options.map((option) => (
          <button
            key={option.value}
            onClick={() => onChange(option.value)}
            className={cn(
              "px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200",
              value === option.value
                ? "glass-strong text-primary border-primary/50"
                : "glass hover:glass-strong text-muted-foreground hover:text-foreground"
            )}
          >
            {option.label}
          </button>
        ))}
      </div>
    </div>
  );
}
