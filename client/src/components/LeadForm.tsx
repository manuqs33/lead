import { useState } from "react";
import { DegreeForm } from "./DegreeForm";
import { Lead, useFormContextLead } from "../hooks/FormHooks";
/* import { PostLead } from "../api/LeadApi"; */


export const LeadForm = () => {
    const {
        register,
        formState: { errors },
        handleSubmit,
    } = useFormContextLead()
    const [showModal, setShowModal] = useState(false);
    const [leadId, setLeadId] = useState(null);

    const handleClose = () => setShowModal(false);

    const onSubmit = async (data: Lead) => {
        
        console.log(data);
        setLeadId(null);
        /* const responseData = await PostLead(data);
        console.log(responseData);

        if (responseData) {
            setLeadId(responseData.id);
            setShowModal(true);
        } */
    };
    
    return (
        <div>
            <form onSubmit={handleSubmit(onSubmit)} className="container mt-4">
                <div className="mb-3">
                    <label htmlFor="full_name" className="form-label">Nombre completo</label>
                    <input
                        type="text"
                        id="full_name"
                        className={`form-control ${errors.full_name ? 'is-invalid' : ''}`}
                        {...register('full_name')}
                    />
                    {errors.full_name && <div className="invalid-feedback">{errors.full_name.message}</div>}
                </div>

                <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email</label>
                    <input
                        type="email"
                        id="email"
                        className={`form-control ${errors.email ? 'is-invalid' : ''}`}
                        {...register('email')}
                    />
                    {errors.email && <div className="invalid-feedback">{errors.email.message}</div>}
                </div>

                <div className="mb-3">
                    <label htmlFor="address" className="form-label">Dirección</label>
                    <input
                        type="text"
                        id="address"
                        className={`form-control ${errors.address ? 'is-invalid' : ''}`}
                        {...register('address')}
                    />
                    {errors.address && <div className="invalid-feedback">{errors.address.message}</div>}
                </div>

                <div className="mb-3">
                    <label htmlFor="phone" className="form-label">Teléfono</label>
                    <input
                        type="text"
                        id="phone"
                        className={`form-control ${errors.phone ? 'is-invalid' : ''}`}
                        {...register('phone')}
                    />
                    {errors.phone && <div className="invalid-feedback">{errors.phone.message}</div>}
                </div>
                <hr />
                <DegreeForm />
                <div className="submit-container">
                    <button type="submit" className="btn btn-lg btn-info">Registrar lead</button>
                </div>
            </form>

            {showModal && (
                <div className="modal fade show d-block" role="dialog">
                    <div className="modal-dialog" role="document">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">Lead creado correctamente</h5>
                            </div>
                            <div className="modal-body">
                                <p>el lead, sus carreras y materias se crearon con éxito con el Id: {leadId}</p>
                            </div>
                            <div className="modal-footer">
                                <button type="button" className="btn btn-secondary" onClick={handleClose}>Close</button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};