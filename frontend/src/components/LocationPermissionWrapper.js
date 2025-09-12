import React from 'react';
import LocationPermission from './LocationPermission';

const LocationPermissionWrapper = ({ onLocationGranted }) => {
  return (
    <div className="fixed inset-0 flex items-start justify-center z-[1001] bg-gradient-to-b from-black/20 to-transparent px-4">
      <div className="mt-24 md:mt-28 mb-20 md:mb-28">
        <LocationPermission onLocationGranted={onLocationGranted} />
      </div>
    </div>
  );
};

export default LocationPermissionWrapper;
