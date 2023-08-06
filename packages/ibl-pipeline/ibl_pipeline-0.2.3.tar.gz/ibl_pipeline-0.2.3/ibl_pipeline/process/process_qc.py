from ibl_pipeline.process import update_utils, ingest_alyx_raw
from ibl_pipeline.ingest import alyxraw
from ibl_pipeline import acquisition, qc
from ibl_pipeline.ingest import qc as qc_ingest
from ibl_pipeline.process.ingest_real import copy_table
import logging

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("/src/IBL-pipeline/ibl_pipeline/process/logs/process_qc.log"),
        logging.StreamHandler()],
    level=25)

logger = logging.getLogger(__name__)

alyx_model = 'actions.session'


def delete_qc_entries():

    qc_keys = update_utils.get_deleted_keys(alyx_model) + \
        update_utils.get_updated_keys(alyx_model, fields=['qc', 'extended_qc'])

    logger.log(25, 'Deleting updated qc and extended_qc from alyxraw...')
    (alyxraw.AlyxRaw.Field &
     'fname in ("qc", "extended_qc")' & qc_keys).delete_quick()

    logger.log(25, 'Deleting updated qc and extended_qc from shadow tables')
    session_uuids = [{'session_uuid': k['uuid']} for k in qc_keys]
    sessions = acquisition.Session & session_uuids
    (qc_ingest.SessionQCIngest & session_uuids).delete_quick()
    (qc_ingest.SessionQC & sessions).delete_quick()
    (qc_ingest.SessionExtendedQC.Field & sessions).delete_quick()
    (qc_ingest.SessionExtendedQC & sessions).delete_quick()

    logger.log(25, 'Deleting updated qc and extended_qc from real tables')
    (qc.SessionExtendedQC.Field & sessions).delete_quick()
    (qc.SessionExtendedQC & sessions).delete_quick()
    (qc.SessionQC & sessions).delete_quick()


def process_alyxraw_qc(
        filename='/data/alyxfull.json',
        models=['actions.session']):
    '''
    Ingest all qc entries in a particular alyx dump, regardless of the current status.
    '''

    ingest_alyx_raw.insert_to_alyxraw(
        ingest_alyx_raw.get_alyx_entries(
            filename=filename,
            models=models
        ),
        alyx_type='part'
    )


def ingest_shadow_tables():

    qc_ingest.SessionQCIngest.populate(
        display_progress=True, suppress_errors=True)


def ingest_real_tables():

    QC_TABLES = ['SessionQC', 'SessionExtendedQC', 'SessionExtendedQC.Field']

    for t in QC_TABLES:
        copy_table(qc, qc_ingest, t)


def main(fpath='/data/alyxfull.json'):

    logger.log(25, 'Insert to update alyxraw...')
    update_utils.insert_to_update_alyxraw(
        filename=fpath, delete_tables=True,
        models=['actions.session'])

    logger.log(25, 'Deleting updated entries...')
    delete_qc_entries()

    logger.log(25, 'Ingesting Alyxraw for QC...')
    process_alyxraw_qc()

    logger.log(25, 'Ingesting QC shadow tables...')
    ingest_shadow_tables()

    logger.log(25, 'Copying real tables...')
    ingest_real_tables()


if __name__ == '__main__':

    main()
