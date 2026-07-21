import React, { useState, useEffect } from 'react';
import { getStoredToken } from '../../services/authService';

interface AuthImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  src: string;
}

const AuthenticatedImage: React.FC<AuthImageProps> = ({ src, ...props }) => {
  const [imgSrc, setImgSrc] = useState<string>('');

  useEffect(() => {
    let objectUrl: string;
    const fetchImage = async () => {
      try {
        const token = getStoredToken();
        const headers: HeadersInit = {};
        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }
        const res = await fetch(src, { headers });
        if (!res.ok) throw new Error('Failed to fetch image');
        const blob = await res.blob();
        objectUrl = URL.createObjectURL(blob);
        setImgSrc(objectUrl);
      } catch (err) {
        console.error('Error fetching authenticated image:', err);
      }
    };

    if (src) {
      if (src.includes('/evaluador/feedback/screenshots/')) {
        fetchImage();
      } else {
        setImgSrc(src);
      }
    }

    return () => {
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [src]);

  return <img src={imgSrc || src} {...props} />;
};

export default AuthenticatedImage;
