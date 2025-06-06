import React, { useEffect, useState } from "react";
import StudentPatientTable from "../components/StudentPatientTable";

const StudentDash = () => {


  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Expedientes disponibles</h1>
      <p className="mb-6 text-gray-600">Selecciona un expediente para comenzar a llenarlo.</p>

     <StudentPatientTable />  
    </div>
  );
};

export default StudentDash;