import React from 'react';
import { Modal, Form, Input, Button } from 'antd';

const EditCircleModal = ({
  open,
  onClose,
  onSubmit,
  selectedCircle,
  updateData,
  setUpdateData,
  newCircle,
  setNewCircle,
  openDeleteModal
}) => {
  return (
    <Modal
      title={selectedCircle ? 'Edit Circle' : 'Create Circle'}
      open={open}
      onCancel={onClose}
      footer={null}
    >
      <Form
        initialValues={selectedCircle ? { name: updateData.name } : { name: '' }}
        onFinish={onSubmit}
      >
        <Form.Item
          label="Name"
          name="name"
          rules={[{ required: true, message: 'Please input the name!' }]}
        >
          <Input
            value={selectedCircle ? updateData.name : newCircle}
            onChange={(e) =>
              selectedCircle
                ? setUpdateData({ ...updateData, name: e.target.value })
                : setNewCircle(e.target.value)
            }
          />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            {selectedCircle ? 'Update' : 'Create'}
          </Button>
          {selectedCircle && (
            <Button type="danger" onClick={() => openDeleteModal(selectedCircle)}>
              Delete
            </Button>
          )}
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default EditCircleModal;