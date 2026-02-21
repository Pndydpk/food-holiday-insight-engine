// components/dashboard/holidayMap.ts

export const FOOD_HOLIDAYS: Record<string, string> = {
  "2026-01-29": "National Corn Chip Day",
  "2026-01-30": "National Croissant Day",
  "2026-02-09": "National Pizza Day",
};

export function formatDateKey(date: Date) {
  return date.toISOString().split("T")[0];
}