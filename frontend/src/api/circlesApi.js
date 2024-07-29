import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

const baseUrl = import.meta.env.VITE_API_URL;

export const circlesApi = createApi({
  reducerPath: 'circlesApi',
  baseQuery: fetchBaseQuery({ baseUrl: `${baseUrl}/api` }),
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
