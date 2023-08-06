from enum import Enum

class AssetFileType(Enum):
    video = 0
    audio = 1
    image = 2
    subtitles = 3
    document = 4

class AuthorisationLevel(Enum):
    user = 0
    workflow = 1
    superAdmin = 2

class CommentType(Enum):
    general = 0
    video = 1
    audio = 2

class CostsGroupBy(Enum):
    none = 0
    blidget = 1
    campaign = 2
    costCentre = 3
    costTrackedService = 4
    fileStore = 5
    organisation = 6
    rate = 7
    transactionType = 8
    workOrder = 9
    day = 10
    week = 11
    month = 12
    quarter = 13
    year = 14

class CostsReportType(Enum):
    currency = 0
    measurement = 1
    frequency = 2

class CostsTransactionType(Enum):
    purchase = 0
    sale = 1
    all = 2

class EntityDeletionRestriction(Enum):
    entityInUse = 0
    requiredBySystem = 1

class FileStoreStatus(Enum):
    new = 0
    error = 1
    ok = 2

class FileTokenType(Enum):
    browseProxyToken = 0
    streamingServiceToken = 1
    downloadToken = 2
    previewPlayerToken = 3
    workflowFileStreamToken = 4

class FolderStructureDepth(Enum):
    contents = 0
    shallow = 1
    full = 2

class MetadataFieldType(Enum):
    boolean = 0
    number = 1
    text = 2
    choice = 3
    date = 4
    longText = 5
    timecode = 6
    multi = 7
    time = 8
    dateTime = 9

class OperationType(Enum):
    create = 0
    read = 1
    update = 2
    delete = 3
    info = 4
    error = 5
    other = 6

class QcMarkerLevel(Enum):
    info = 0
    warning = 1
    failuer = 2

class QcMarkerType(Enum):
    result = 0
    general = 1
    audio = 2
    video = 3

class RecorderStatus(Enum):
    idle = 0
    inUse = 1

class ReviewTaskResult(Enum):
    passed = 0
    failed = 1

class RunNodeStatus(Enum):
    pending = 0
    running = 1
    completed = 2
    failed = 3
    queued = 4
    cancelled = 5
    idle = 6

class ScheduledRecordingStatus(Enum):
    scheduled = 0
    inProgress = 1
    completed = 2
    cancelled = 3
    failed = 4

class TaskStatus(Enum):
    pending = 0
    inProgress = 1
    completed = 2
    rejected = 3

class WorkflowRunStatus(Enum):
    running = 0
    complete = 1
    failed = 2

class WorkOrderStatus(Enum):
    pending = 0
    started = 1
    error = 2
    completed = 3
    rejected = 4
    cancelled = 5