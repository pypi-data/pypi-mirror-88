from azureml.studio.internal.error import ErrorMapping, InvalidDatasetError, ModuleOutOfMemoryError


def raise_error(e, mode='Training'):
    if isinstance(e, RuntimeError):
        ex_msg = str(e.args).lower()
        if "sizes of tensors must match" in ex_msg:
            ErrorMapping.rethrow(
                e,
                InvalidDatasetError(
                    dataset1=f"{mode} dataset",
                    reason=f"Got exception when {mode.lower()}: {ErrorMapping.get_exception_message(e)}",
                    troubleshoot_hint="Please transform input images to have the same size, see "
                                      "https://aka.ms/aml/init-image-transformation."))

        if any(err_msg.lower() in ex_msg for err_msg in ["CUDA out of memory", "can't allocate memory"]):
            ErrorMapping.rethrow(
                e,
                ModuleOutOfMemoryError(f"Cannot allocate more memory because {ErrorMapping.get_exception_message(e)}. "
                                       f"Please reduce hyper-parameter 'Batch size', or upgrade VM Sku."))

    raise e
