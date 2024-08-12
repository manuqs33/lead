import { useFieldArray } from "react-hook-form";
import { useFormContextLead } from "../hooks/FormHooks";
import { Fragment } from "react/jsx-runtime";
import { SubjectForm } from "./SubjectForm";



export const DegreeForm = () => {
    const {
        register,
        control,
        formState: { errors },
    } = useFormContextLead();

    const { append, remove, fields } = useFieldArray({
        name: 'degrees',
        control,
    })

    return (
        <div className='my-4'>
            {fields.map((degree, degreeIndex) => {
                return (
                    <Fragment key={degree.id || degreeIndex}>
                        <div className="mb-3">
                        <div className='flex-between'>
                            <h3 className='mb-2'>Carrera {degreeIndex + 1}</h3>{' '}
                            <button
                                type='button'
                                onClick={() => {
                                    remove(degreeIndex)
                                }}
                                className='btn btn-secondary'
                            >
                                Remover carrera
                            </button>
                        </div>
                            <label htmlFor={`degrees.${degreeIndex}.name`} className="form-label">Degree Name</label>
                            <input
                                type="text"
                                id={`degrees.${degreeIndex}.name`}
                                {...register(`degrees.${degreeIndex}.name`)}
                                className={`form-control ${errors.degrees?.[degreeIndex]?.name ? 'is-invalid' : ''}`}
                            />
                            {errors.degrees?.[degreeIndex]?.name && (
                                <div className="invalid-feedback">
                                    {errors.degrees[degreeIndex].name.message}
                                </div>
                            )}
                        </div>
                        <hr />
                        <SubjectForm degreeIndex={degreeIndex} />
                    </Fragment>
                );
            })}
            <button
                type='button'
                className='btn btn-primary'
                onClick={() => append({ name: '' })}
            >
                Agregar carrera
            </button>
        </div>
    );
};