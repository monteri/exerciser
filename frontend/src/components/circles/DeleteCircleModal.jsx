import { Modal } from 'antd';

const DeleteCircleModal = ({ open, onConfirm, onCancel, selectedCircle }) => {
  return (
    <Modal
      title="Confirm Delete"
      open={open}
      onOk={onConfirm}
      onCancel={onCancel}
      okText="Yes, Delete"
      cancelText="Cancel"
    >
      <p>Are you sure you want to delete {selectedCircle?.name}?</p>
    </Modal>
  );
};

export default DeleteCircleModal;