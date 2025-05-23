'use client';

import React from 'react';

export default function ComplianceBadge({ tags }: { tags: string | string[] }) {
  if (!tags) return null;
  const tagList = Array.isArray(tags) ? tags : [tags];
  return (
    <span className="space-x-1">
      {tagList.map(tag => (
        <span key={tag} className="inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-medium">
          {tag}
        </span>
      ))}
    </span>
  );
}
