import { useState } from "react";
import {
  useListCirclesQuery,
  useCreateCircleMutation,
  useUpdateCircleMutation,
  useDeleteCircleMutation
} from "../api/circlesApi";
import CirclePack from '../components/circles/CirclePack';
import EditCircleModal from '../components/circles/EditCircleModal';
import DeleteCircleModal from '../components/circles/DeleteCircleModal';
import { Button } from 'antd';

const data = {
  name: 'Root',
  children: [
    {
      name: 'User 1',
      value: 1,
      children: [
        { name: 'Sub-item 1', value: 1 },
        { name: 'Sub-item 2', value: 1 },
      ],
    },
    {
      name: 'User 2',
      value: 1,
      children: [
        { name: 'Sub-item 3', value: 1 },
        { name: 'Sub-item 4', value: 1 },
        { name: 'Sub-item 5', value: 1 },
      ],
    },
    {
      name: 'User 3',
      value: 1,
      children: [
        { name: 'Sub-item 1 user 3', value: 1 },
      ],
    },
  ],
};

const PersonalPage = () => {
  const { data: circles, isLoading, error } = useListCirclesQuery();
  const [createCircle] = useCreateCircleMutation();
  const [updateCircle] = useUpdateCircleMutation();
  const [deleteCircle] = useDeleteCircleMutation();

  const [newCircle, setNewCircle] = useState('');
  const [updateData, setUpdateData] = useState({ id: '', name: '' });
  const [selectedCircle, setSelectedCircle] = useState(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

  const handleCreateCircle = async (values) => {
    try {
      await createCircle({ name: values.name }).unwrap();
      setNewCircle('');
      setIsEditModalOpen(false);
    } catch (err) {
      console.error('Failed to create circle:', err);
    }
  };

  const handleUpdateCircle = async (values) => {
    try {
      await updateCircle({ circleId: updateData.id, name: values.name }).unwrap();
      setUpdateData({ id: '', name: '' });
      setIsEditModalOpen(false);
    } catch (err) {
      console.error('Failed to update circle:', err);
    }
  };

  const handleDeleteCircle = async () => {
    try {
      await deleteCircle(selectedCircle.id).unwrap();
      setSelectedCircle(null);
      setIsDeleteModalOpen(false);
    } catch (err) {
      console.error('Failed to delete circle:', err);
    }
  };

  const openEditModal = (circle) => {
    setSelectedCircle(circle);
    setUpdateData({ id: circle.id, name: circle.name });
    setIsEditModalOpen(true);
  };

  const openDeleteModal = (circle) => {
    setSelectedCircle(circle);
    setIsDeleteModalOpen(true);
  };

  const closeModal = () => {
    setSelectedCircle(null);
    setIsEditModalOpen(false);
    setIsDeleteModalOpen(false);
  };

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <div style={{display: "flex", justifyContent: "space-between"}}>
        <h1>Welcome to the Personal Page</h1>
        <Button
          style={{ marginTop: '1rem' }}
          type="primary"
          onClick={() => setIsEditModalOpen(true)}
        >
          Add New Circle
        </Button>
      </div>

      <div style={{ display: "flex", width: "100%", justifyContent: "center" }}>
        <CirclePack data={data} onCircleClick={openEditModal}/>
      </div>

      <EditCircleModal
        open={isEditModalOpen}
        onClose={closeModal}
        onSubmit={selectedCircle ? handleUpdateCircle : handleCreateCircle}
        selectedCircle={selectedCircle}
        updateData={updateData}
        setUpdateData={setUpdateData}
        newCircle={newCircle}
        setNewCircle={setNewCircle}
        openDeleteModal={openDeleteModal}
      />

      <DeleteCircleModal
        open={isDeleteModalOpen}
        onConfirm={handleDeleteCircle}
        onCancel={closeModal}
        selectedCircle={selectedCircle}
      />
    </div>
  );
};

export default PersonalPage;