# Queue Overflow Handling Implementation

## Overview

This implementation provides comprehensive overflow handling for the BFSI API event queue, ensuring no critical events are lost when the queue reaches capacity. The solution includes persistent storage, priority-based handling, and recovery mechanisms.

## Problem Solved

**Original Issue**: When the event queue was full, events were simply dropped, risking critical BFSI data loss.

**Solution**: Implemented a multi-layered overflow handling system that:
- Persists overflow events to durable storage
- Implements priority-based event classification
- Provides recovery mechanisms for stored events
- Ensures critical events are never lost

## Key Components

### 1. Event Priority Classification
**Location**: `realtime_bfsi_api.py` (lines 248-278)

```python
class EventPriority:
    CRITICAL = 1    # System failures, security breaches, regulatory violations
    HIGH = 2        # Transaction failures, compliance issues, risk alerts
    MEDIUM = 3      # Performance issues, operational alerts
    LOW = 4         # General notifications, status updates
```

**Features**:
- Automatic priority detection based on event type
- Content-based priority analysis for critical keywords
- Configurable priority thresholds

### 2. Persistent Overflow Storage
**Location**: `realtime_bfsi_api.py` (lines 280-451)

**Database Schema**:
```sql
CREATE TABLE overflow_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT UNIQUE NOT NULL,
    event_type TEXT NOT NULL,
    priority INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    source_system TEXT,
    data TEXT NOT NULL,
    created_at TEXT NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    retry_count INTEGER DEFAULT 0,
    error_message TEXT
)
```

**Features**:
- SQLite-based persistent storage
- Priority-based event ordering
- Retry count tracking
- Automatic cleanup of old events
- Efficient indexing for fast queries

### 3. Intelligent Queue Overflow Handling
**Location**: `realtime_bfsi_api.py` (lines 1762-1802)

**New Overflow Logic**:
1. **Event Storage**: Store overflow events in persistent database
2. **Priority Handling**: For critical/high priority events, attempt to make room
3. **Graceful Degradation**: Fall back to old behavior if storage fails
4. **Success Response**: Return success with overflow notification

**Key Improvements**:
- No more event dropping
- Priority-based queue management
- Persistent storage ensures data recovery
- Comprehensive logging and monitoring

### 4. Critical Event Room Making
**Location**: `realtime_bfsi_api.py` (lines 453-495)

**Algorithm**:
1. Remove lower priority events from queue
2. Store removed events in overflow storage
3. Add critical event to queue
4. Handle edge cases and failures gracefully

**Features**:
- Intelligent priority comparison
- Batch processing for efficiency
- Error handling and logging
- Fallback mechanisms

### 5. Management Endpoints
**Location**: `realtime_bfsi_api.py` (lines 2528-2706)

#### GET `/overflow-events`
- Retrieve overflow events with filtering
- Support for processed/unprocessed filtering
- Configurable result limits

#### POST `/overflow-events/{event_id}/process`
- Manually process individual overflow events
- Queue integration with error handling
- Retry count management

#### POST `/overflow-events/process-all`
- Batch processing of overflow events (admin only)
- Bulk queue integration
- Comprehensive error reporting

#### DELETE `/overflow-events/cleanup`
- Clean up old processed events (admin only)
- Configurable retention periods
- Database maintenance

#### GET `/overflow-events/stats`
- Comprehensive overflow statistics
- Priority distribution analysis
- Recent activity monitoring

## Event Priority Classification

### Critical Events (Priority 1)
- `security_breach`
- `system_failure`
- `regulatory_violation`
- Events containing keywords: "breach", "failure", "violation", "critical", "urgent"

### High Priority Events (Priority 2)
- `transaction_failure`
- `compliance_alert`
- `risk_threshold_exceeded`

### Medium Priority Events (Priority 3)
- `performance_degradation`
- `operational_alert`

### Low Priority Events (Priority 4)
- All other event types
- General notifications and status updates

## Overflow Handling Flow

### 1. Normal Operation
```
Event → Queue (if space available) → Success
```

### 2. Queue Full - Low Priority Event
```
Event → Queue Full → Store in Overflow DB → Return Success with Notification
```

### 3. Queue Full - Critical/High Priority Event
```
Event → Queue Full → Store in Overflow DB → Try to Make Room → 
  Remove Lower Priority Events → Store Removed Events → Add Critical Event → Success
```

### 4. Storage Failure
```
Event → Queue Full → Storage Fails → Fallback to Old Behavior → 
  Remove Oldest Event → Add New Event → Return 503 Error
```

## Database Schema Details

### Table: `overflow_events`
- **id**: Auto-incrementing primary key
- **event_id**: Unique event identifier
- **event_type**: Type of BFSI event
- **priority**: Calculated priority level (1-4)
- **timestamp**: Original event timestamp
- **source_system**: System that generated the event
- **data**: JSON-encoded event data
- **created_at**: When event was stored in overflow
- **processed**: Whether event has been successfully processed
- **retry_count**: Number of processing attempts
- **error_message**: Last error encountered during processing

### Indexes
- `idx_priority`: For efficient priority-based queries
- `idx_processed`: For filtering processed/unprocessed events
- `idx_timestamp`: For time-based queries and cleanup

## API Response Examples

### Successful Event with Overflow
```json
{
  "message": "Event queued successfully",
  "event_id": "evt_12345",
  "status": "queued_with_overflow",
  "overflow_stored": true,
  "priority": 1,
  "note": "Event stored in persistent overflow storage due to queue capacity"
}
```

### Overflow Statistics
```json
{
  "total_events": 150,
  "pending_events": 25,
  "processed_events": 125,
  "recent_events_24h": 45,
  "priority_distribution": {
    "critical": 5,
    "high": 12,
    "medium": 6,
    "low": 2
  }
}
```

## Monitoring and Alerting

### Key Metrics to Monitor
- **Overflow Rate**: Percentage of events going to overflow storage
- **Priority Distribution**: Distribution of events by priority level
- **Processing Success Rate**: Percentage of overflow events successfully processed
- **Retry Counts**: Number of events requiring multiple processing attempts
- **Storage Health**: Database size and performance metrics

### Log Messages
- **INFO**: Successful overflow storage and processing
- **WARNING**: Queue full conditions and priority handling
- **ERROR**: Storage failures and processing errors
- **DEBUG**: Detailed priority calculations and room-making logic

## Configuration Options

### Database Settings
- **Database Path**: `overflow_events.db` (configurable)
- **Retention Period**: 7 days (configurable)
- **Cleanup Frequency**: Manual or scheduled

### Priority Settings
- **Critical Keywords**: Configurable list of critical terms
- **Priority Thresholds**: Adjustable priority levels
- **Room Making**: Configurable number of events to remove

### Queue Settings
- **Queue Size**: Inherited from existing configuration
- **Processing Limits**: Configurable batch processing limits
- **Retry Logic**: Configurable retry counts and delays

## Security Considerations

### Access Control
- **Read Access**: All authenticated users can view overflow events
- **Process Access**: All authenticated users can process individual events
- **Admin Access**: Only admins can batch process and cleanup
- **Audit Logging**: All overflow operations are logged

### Data Protection
- **Encryption**: Event data stored as JSON (can be encrypted)
- **Retention**: Configurable data retention periods
- **Cleanup**: Automatic cleanup of old processed events
- **Backup**: Database can be backed up independently

## Performance Considerations

### Database Performance
- **Indexing**: Optimized indexes for common queries
- **Connection Pooling**: Reuses database connections
- **Batch Operations**: Efficient batch processing
- **Cleanup**: Regular cleanup prevents database bloat

### Queue Performance
- **Non-blocking**: Overflow handling doesn't block normal operations
- **Priority Processing**: Critical events get priority treatment
- **Efficient Storage**: Minimal overhead for overflow storage
- **Recovery**: Fast recovery of stored events

## Testing and Validation

### Unit Tests
- Priority classification accuracy
- Database operations
- Queue integration
- Error handling

### Integration Tests
- End-to-end overflow scenarios
- Priority-based room making
- Batch processing
- Recovery mechanisms

### Load Tests
- High-volume event processing
- Queue capacity testing
- Database performance under load
- Recovery time testing

## Future Enhancements

### Potential Improvements
1. **Redis Integration**: Use Redis for overflow storage for better performance
2. **Message Queues**: Integrate with external message queues (RabbitMQ, Kafka)
3. **Machine Learning**: AI-based priority classification
4. **Real-time Monitoring**: Live dashboards for overflow statistics
5. **Auto-scaling**: Automatic queue size adjustment based on load

### Advanced Features
1. **Event Deduplication**: Prevent duplicate events in overflow
2. **Compression**: Compress stored event data
3. **Encryption**: Encrypt sensitive event data
4. **Replication**: Replicate overflow storage for high availability
5. **Analytics**: Advanced analytics on overflow patterns

## Deployment Notes

### Prerequisites
- SQLite database support
- Sufficient disk space for overflow storage
- Monitoring and alerting setup
- Backup procedures for overflow database

### Configuration
- Set appropriate retention periods
- Configure priority thresholds
- Set up monitoring dashboards
- Test overflow scenarios

### Maintenance
- Regular database cleanup
- Monitor overflow statistics
- Review priority classifications
- Update configuration as needed

This implementation ensures that no critical BFSI events are ever lost, providing robust overflow handling with comprehensive monitoring and recovery capabilities.
