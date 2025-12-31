import React, { useState, useRef } from 'react';
import './MelodyUpload.css';

interface MelodyUploadProps {
  onUpload: (file: File) => void;
  isLoading?: boolean;
}

const MelodyUpload: React.FC<MelodyUploadProps> = ({ onUpload, isLoading = false }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file: File) => {
    const validExtensions = ['.xml', '.musicxml', '.mscz'];
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();

    if (!validExtensions.includes(fileExtension)) {
      alert('Please upload a valid file (.xml, .musicxml, or .mscz)');
      return;
    }

    setSelectedFile(file);
    onUpload(file);
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="melody-upload">
      <h3>Upload Melody</h3>
      <div
        className={`upload-zone ${dragActive ? 'drag-active' : ''} ${isLoading ? 'loading' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleButtonClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".xml,.musicxml,.mscz"
          onChange={handleChange}
          style={{ display: 'none' }}
          disabled={isLoading}
        />

        {isLoading ? (
          <div className="upload-loading">
            <div className="spinner"></div>
            <p>Analyzing melody...</p>
          </div>
        ) : selectedFile ? (
          <div className="upload-success">
            <div className="file-icon">📄</div>
            <p className="file-name">{selectedFile.name}</p>
            <p className="file-size">{(selectedFile.size / 1024).toFixed(2)} KB</p>
            <button className="change-file-btn">Change file</button>
          </div>
        ) : (
          <div className="upload-prompt">
            <div className="upload-icon">🎵</div>
            <p className="upload-title">Drag & drop your melody file here</p>
            <p className="upload-subtitle">or click to browse</p>
            <p className="upload-formats">Supported formats: MusicXML (.xml, .musicxml), MuseScore (.mscz)</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MelodyUpload;
