import { createApi } from '@reduxjs/toolkit/query/react';
import baseQueryWithReauth from "./fetchBaseQuery.js";

export const circlesApi = createApi({
  reducerPath: 'circlesApi',
  baseQuery: baseQueryWithReauth,
  endpoints: (builder) => ({
    listCircles: builder.query({
      query: () => 'circles/',
    }),
    createCircle: builder.mutation({
      query: (newCircle) => ({
        url: 'circles/',
        method: 'POST',
        body: newCircle,
      }),
    }),
    retrieveCircle: builder.query({
      query: (circleId) => `circles/${circleId}/`,
    }),
    updateCircle: builder.mutation({
      query: ({ circleId, ...updatedCircle }) => ({
        url: `circles/${circleId}/`,
        method: 'PUT',
        body: updatedCircle,
      }),
    }),
    deleteCircle: builder.mutation({
      query: (circleId) => ({
        url: `circles/${circleId}/`,
        method: 'DELETE',
      }),
    }),
    searchCircles: builder.query({
      query: (query) => `search/?q=${query}`,
    }),
  }),
});

export const {
  useListCirclesQuery,
  useCreateCircleMutation,
  useRetrieveCircleQuery,
  useUpdateCircleMutation,
  useDeleteCircleMutation,
  useSearchCirclesQuery,
} = circlesApi;
