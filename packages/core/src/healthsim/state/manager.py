"""
HealthSim State Manager - DuckDB Backend.

Provides save/load/list/delete operations for scenarios using DuckDB
as the storage backend instead of JSON files.

Extended with auto-persist capabilities for token-efficient scenario management.
"""

from typing import Any, Dict, List, Optional, Union
from uuid import uuid4
from datetime import datetime
from pathlib import Path
import json

import duckdb

from ..db import get_connection
from .serializers import (
    get_serializer,
    get_table_info,
    ENTITY_TABLE_MAP,
)
from .auto_persist import (
    AutoPersistService,
    PersistResult,
    QueryResult,
    ScenarioBrief,
    get_auto_persist_service,
)
from .summary import ScenarioSummary


class StateManager:
    """
    Manages scenario persistence in DuckDB.
    
    Scenarios are collections of entities (patients, encounters, claims, etc.)
    that can be saved, loaded, listed, and deleted. Entity data is stored both:
    1. In typed canonical tables (patients, encounters, etc.) for SQL queries
    2. In scenario_entities.entity_data as JSON for round-trip compatibility
    
    Extended Features (Auto-Persist):
    - `persist()` - Token-efficient persist that stores in canonical tables
    - `get_summary()` - Load only summary (~500 tokens) instead of full data
    - `query()` - Run SQL queries against scenario data with pagination
    
    Usage:
        manager = StateManager()
        
        # Traditional save/load (full data in context)
        scenario_id = manager.save_scenario(
            name='diabetes-cohort',
            entities={'patients': [...], 'encounters': [...]},
        )
        scenario = manager.load_scenario('diabetes-cohort')  # Full data
        
        # Auto-persist pattern (token-efficient)
        result = manager.persist(
            entities={'patients': [...], 'encounters': [...]},
            context='diabetes patients in San Diego'
        )
        # Returns summary (~500 tokens), not full data
        
        summary = manager.get_summary('diabetes-patients-20241227')
        # Query for specific data
        results = manager.query(scenario_id, "SELECT * FROM patients WHERE gender = 'F'")
    """
    
    def __init__(self, connection: Optional[duckdb.DuckDBPyConnection] = None):
        """
        Initialize state manager.
        
        Args:
            connection: Optional database connection (uses default if not provided)
        """
        self._conn = connection
        self._auto_persist: Optional[AutoPersistService] = None
    
    @property
    def conn(self) -> duckdb.DuckDBPyConnection:
        """Get database connection (lazy initialization)."""
        if self._conn is None:
            self._conn = get_connection()
        return self._conn
    
    @property
    def auto_persist(self) -> AutoPersistService:
        """Get auto-persist service (lazy initialization)."""
        if self._auto_persist is None:
            self._auto_persist = AutoPersistService(self.conn)
        return self._auto_persist
    
    # =========================================================================
    # Auto-Persist Methods (Token-Efficient)
    # =========================================================================
    
    def persist(
        self,
        entities: Dict[str, List[Dict]],
        scenario_id: Optional[str] = None,
        scenario_name: Optional[str] = None,
        context: Optional[str] = None,
        tags: Optional[List[str]] = None,
        description: Optional[str] = None,
    ) -> PersistResult:
        """
        Persist entities using the auto-persist pattern.
        
        This is the recommended method for token-efficient scenario management.
        Entities are stored directly in canonical tables with scenario_id.
        Returns a summary instead of echoing back all data.
        
        Args:
            entities: Dict mapping entity type to list of entities
            scenario_id: Optional existing scenario to add to
            scenario_name: Optional explicit scenario name
            context: Context string for auto-naming (e.g., 'diabetes patients')
            tags: Optional tags for organization
            description: Optional description
            
        Returns:
            PersistResult with summary and entity IDs (not full data)
            
        Example:
            result = manager.persist(
                entities={'patients': patient_list},
                context='diabetes cohort San Diego',
                tags=['diabetes', 'san-diego']
            )
            # result.summary has ~500 tokens, not 10K+ for full data
        """
        return self.auto_persist.persist_entities(
            entities=entities,
            scenario_id=scenario_id,
            scenario_name=scenario_name,
            context=context,
            tags=tags,
            description=description,
        )
    
    def get_summary(
        self,
        scenario_id_or_name: str,
        include_samples: bool = True,
        samples_per_type: int = 3,
    ) -> ScenarioSummary:
        """
        Get a token-efficient summary of a scenario.
        
        Use this instead of load_scenario() when you need context
        about a scenario without loading all entities.
        
        Args:
            scenario_id_or_name: Scenario identifier (UUID or name)
            include_samples: Whether to include sample entities
            samples_per_type: Number of samples per entity type
            
        Returns:
            ScenarioSummary with counts, statistics, and optional samples
            - Without samples: ~500 tokens
            - With samples: ~3,500 tokens
            
        Example:
            summary = manager.get_summary('diabetes-patients-20241227')
            print(f"Scenario has {summary.total_entities()} entities")
            print(f"Token cost: ~{summary.token_estimate()} tokens")
        """
        return self.auto_persist.get_scenario_summary(
            scenario_id_or_name=scenario_id_or_name,
            include_samples=include_samples,
            samples_per_type=samples_per_type,
        )
    
    def query(
        self,
        scenario_id_or_name: str,
        sql: str,
        limit: int = 20,
        offset: int = 0,
    ) -> QueryResult:
        """
        Run a SQL query against scenario data with pagination.
        
        Only SELECT queries are allowed. Queries are automatically
        filtered to the specified scenario.
        
        Args:
            scenario_id_or_name: Scenario identifier
            sql: SQL SELECT query
            limit: Max results per page (default 20, max 100)
            offset: Pagination offset
            
        Returns:
            QueryResult with rows, columns, and pagination info
            
        Example:
            result = manager.query(
                'diabetes-patients-20241227',
                "SELECT given_name, family_name, birth_date FROM patients WHERE gender = 'F'",
                limit=10
            )
            for row in result.rows:
                print(row)
            if result.has_more:
                # Fetch next page
                result = manager.query(..., offset=10)
        """
        return self.auto_persist.query_scenario(
            scenario_id_or_name=scenario_id_or_name,
            query=sql,
            limit=limit,
            offset=offset,
        )
    
    def get_samples(
        self,
        scenario_id_or_name: str,
        entity_type: str,
        count: int = 3,
        strategy: str = 'diverse',
    ) -> List[Dict]:
        """
        Get sample entities from a scenario.
        
        Args:
            scenario_id_or_name: Scenario identifier
            entity_type: Type of entity to sample
            count: Number of samples (default 3)
            strategy: 'diverse', 'random', or 'recent'
            
        Returns:
            List of entity dicts (without internal fields)
        """
        return self.auto_persist.get_entity_samples(
            scenario_id_or_name=scenario_id_or_name,
            entity_type=entity_type,
            count=count,
            strategy=strategy,
        )
    
    # =========================================================================
    # Traditional Methods (Full Data Loading)
    # =========================================================================
    
    def save_scenario(
        self,
        name: str,
        entities: Dict[str, List[Dict]],
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        overwrite: bool = False,
        product: str = 'healthsim',
    ) -> str:
        """
        Save a scenario to the database (traditional method).
        
        Note: For token-efficient persistence, use persist() instead.
        
        Args:
            name: Unique scenario name
            entities: Dict mapping entity type to list of entities
            description: Optional description
            tags: Optional list of tags for filtering
            overwrite: If True, replace existing scenario with same name
            product: Product identifier (patientsim, membersim, etc.)
            
        Returns:
            Scenario ID (UUID string)
            
        Raises:
            ValueError: If scenario exists and overwrite=False
        """
        # Check for existing scenario
        existing = self._get_scenario_by_name(name)
        if existing and not overwrite:
            raise ValueError(f"Scenario '{name}' already exists. Use overwrite=True to replace.")
        
        scenario_id = existing['scenario_id'] if existing else str(uuid4())
        now = datetime.utcnow()
        
        # If overwriting, clear existing entity links
        if existing and overwrite:
            self._delete_scenario_entities(scenario_id)
            self.conn.execute("DELETE FROM scenario_tags WHERE scenario_id = ?", [scenario_id])
        
        # Build metadata JSON
        metadata = {
            'product': product,
            'entity_types': list(entities.keys()),
            'entity_counts': {k: len(v) for k, v in entities.items()},
        }
        
        # Create or update scenario record
        if existing:
            self.conn.execute("""
                UPDATE scenarios SET
                    description = ?,
                    updated_at = ?,
                    metadata = ?
                WHERE scenario_id = ?
            """, [description, now, json.dumps(metadata), scenario_id])
        else:
            self.conn.execute("""
                INSERT INTO scenarios (scenario_id, name, description, created_at, updated_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [scenario_id, name, description, now, now, json.dumps(metadata)])
        
        # Insert entities
        entity_count = 0
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                self._save_entity(scenario_id, entity_type, entity)
                entity_count += 1
        
        # Save tags
        if tags:
            for tag in tags:
                # Check if tag already exists
                existing = self.conn.execute("""
                    SELECT id FROM scenario_tags WHERE scenario_id = ? AND tag = ?
                """, [scenario_id, tag]).fetchone()
                
                if not existing:
                    self.conn.execute("""
                        INSERT INTO scenario_tags (id, scenario_id, tag)
                        VALUES (nextval('scenario_tags_seq'), ?, ?)
                    """, [scenario_id, tag])
        
        return scenario_id
    
    def load_scenario(self, name_or_id: str) -> Dict[str, Any]:
        """
        Load a scenario from the database (full data).
        
        Note: For token-efficient loading, use get_summary() instead.
        
        Args:
            name_or_id: Scenario name or UUID
            
        Returns:
            Dict with scenario metadata and all entities
            
        Raises:
            ValueError: If scenario not found
        """
        # Try as name first, then as UUID
        scenario = self._get_scenario_by_name(name_or_id)
        if not scenario:
            scenario = self._get_scenario_by_id(name_or_id)
        if not scenario:
            raise ValueError(f"Scenario '{name_or_id}' not found")
        
        scenario_id = scenario['scenario_id']
        
        # Load all entities for this scenario from scenario_entities
        entities = self._load_scenario_entities(scenario_id)
        
        # Load tags
        tags_result = self.conn.execute("""
            SELECT tag FROM scenario_tags WHERE scenario_id = ?
        """, [scenario_id]).fetchall()
        tags = [t[0] for t in tags_result]
        
        # Parse metadata
        metadata = {}
        if scenario.get('metadata'):
            try:
                metadata = json.loads(scenario['metadata']) if isinstance(scenario['metadata'], str) else scenario['metadata']
            except (json.JSONDecodeError, TypeError):
                pass
        
        return {
            'scenario_id': scenario_id,
            'name': scenario['name'],
            'description': scenario['description'],
            'created_at': scenario['created_at'],
            'updated_at': scenario['updated_at'],
            'tags': tags,
            'metadata': metadata,
            'entities': entities,
            'entity_count': sum(len(v) for v in entities.values()),
        }
    
    def list_scenarios(
        self,
        tag: Optional[str] = None,
        search: Optional[str] = None,
        product: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        List available scenarios.
        
        Args:
            tag: Filter by tag
            search: Search in name/description
            product: Filter by product (from metadata)
            limit: Max results (default 100)
            
        Returns:
            List of scenario summaries (without full entity data)
        """
        query = """
            SELECT DISTINCT s.scenario_id, s.name, s.description, 
                   s.created_at, s.updated_at, s.metadata
            FROM scenarios s
        """
        params = []
        conditions = []
        
        if tag:
            query += " JOIN scenario_tags t ON s.scenario_id = t.scenario_id"
            conditions.append("t.tag = ?")
            params.append(tag)
        
        if search:
            conditions.append("(s.name LIKE ? OR s.description LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY s.updated_at DESC LIMIT ?"
        params.append(limit)
        
        results = self.conn.execute(query, params).fetchall()
        
        scenarios = []
        for row in results:
            metadata = {}
            if row[5]:
                try:
                    metadata = json.loads(row[5]) if isinstance(row[5], str) else row[5]
                except (json.JSONDecodeError, TypeError):
                    pass
            
            # Filter by product if specified
            if product and metadata.get('product') != product:
                continue
            
            # Get entity count
            count_result = self.conn.execute("""
                SELECT COUNT(*) FROM scenario_entities WHERE scenario_id = ?
            """, [row[0]]).fetchone()
            
            # Get tags
            tags_result = self.conn.execute("""
                SELECT tag FROM scenario_tags WHERE scenario_id = ?
            """, [row[0]]).fetchall()
            
            scenarios.append({
                'scenario_id': row[0],
                'name': row[1],
                'description': row[2],
                'created_at': row[3],
                'updated_at': row[4],
                'entity_count': count_result[0] if count_result else 0,
                'tags': [t[0] for t in tags_result],
                'metadata': metadata,
            })
        
        return scenarios
    
    def delete_scenario(self, name_or_id: str, confirm: bool = False) -> bool:
        """
        Delete a scenario.
        
        Note: This removes the scenario and all associated entities from
        canonical tables where scenario_id matches.
        
        Args:
            name_or_id: Scenario name or UUID
            confirm: Must be True to actually delete (safety check)
            
        Returns:
            True if deleted, False if not found
        """
        if not confirm:
            raise ValueError("Must pass confirm=True to delete scenario")
        
        scenario = self._get_scenario_by_name(name_or_id) or self._get_scenario_by_id(name_or_id)
        if not scenario:
            return False
        
        scenario_id = scenario['scenario_id']
        
        # Delete from canonical tables (entities with this scenario_id)
        canonical_tables = [
            'patients', 'encounters', 'diagnoses', 'medications',
            'lab_results', 'vital_signs', 'orders', 'clinical_notes',
            'members', 'claims', 'claim_lines',
            'prescriptions', 'pharmacy_claims',
            'subjects', 'trial_visits', 'adverse_events', 'exposures'
        ]
        for table in canonical_tables:
            try:
                self.conn.execute(f"DELETE FROM {table} WHERE scenario_id = ?", [scenario_id])
            except Exception:
                pass  # Table may not have scenario_id column yet
        
        # Delete in order: tags, entity links, scenario
        self.conn.execute("DELETE FROM scenario_tags WHERE scenario_id = ?", [scenario_id])
        self.conn.execute("DELETE FROM scenario_entities WHERE scenario_id = ?", [scenario_id])
        self.conn.execute("DELETE FROM scenarios WHERE scenario_id = ?", [scenario_id])
        
        return True
    
    def rename_scenario(self, old_name_or_id: str, new_name: str) -> bool:
        """
        Rename a scenario.
        
        Args:
            old_name_or_id: Current scenario name or UUID
            new_name: New scenario name
            
        Returns:
            True if renamed successfully
            
        Raises:
            ValueError: If scenario not found or new name already exists
        """
        return self.auto_persist.rename_scenario(old_name_or_id, new_name)
    
    def scenario_exists(self, name_or_id: str) -> bool:
        """Check if a scenario exists."""
        return (
            self._get_scenario_by_name(name_or_id) is not None or
            self._get_scenario_by_id(name_or_id) is not None
        )
    
    def get_scenario_tags(self, name_or_id: str) -> List[str]:
        """Get tags for a scenario."""
        scenario = self._get_scenario_by_name(name_or_id) or self._get_scenario_by_id(name_or_id)
        if not scenario:
            return []
        
        result = self.conn.execute("""
            SELECT tag FROM scenario_tags WHERE scenario_id = ?
        """, [scenario['scenario_id']]).fetchall()
        return [t[0] for t in result]
    
    def add_scenario_tags(self, name_or_id: str, tags: List[str]) -> bool:
        """Add tags to a scenario."""
        scenario = self._get_scenario_by_name(name_or_id) or self._get_scenario_by_id(name_or_id)
        if not scenario:
            return False
        
        for tag in tags:
            # Check if tag already exists
            existing = self.conn.execute("""
                SELECT id FROM scenario_tags WHERE scenario_id = ? AND tag = ?
            """, [scenario['scenario_id'], tag]).fetchone()
            
            if not existing:
                self.conn.execute("""
                    INSERT INTO scenario_tags (id, scenario_id, tag)
                    VALUES (nextval('scenario_tags_seq'), ?, ?)
                """, [scenario['scenario_id'], tag])
        return True
    
    # =========================================================================
    # Private helper methods
    # =========================================================================
    
    def _get_scenario_by_name(self, name: str) -> Optional[Dict]:
        """Get scenario by name."""
        result = self.conn.execute(
            "SELECT scenario_id, name, description, created_at, updated_at, metadata FROM scenarios WHERE name = ?",
            [name]
        ).fetchone()
        if result:
            return {
                'scenario_id': result[0],
                'name': result[1],
                'description': result[2],
                'created_at': result[3],
                'updated_at': result[4],
                'metadata': result[5],
            }
        return None
    
    def _get_scenario_by_id(self, scenario_id: str) -> Optional[Dict]:
        """Get scenario by ID."""
        try:
            result = self.conn.execute(
                "SELECT scenario_id, name, description, created_at, updated_at, metadata FROM scenarios WHERE scenario_id = ?",
                [scenario_id]
            ).fetchone()
            if result:
                return {
                    'scenario_id': result[0],
                    'name': result[1],
                    'description': result[2],
                    'created_at': result[3],
                    'updated_at': result[4],
                    'metadata': result[5],
                }
        except Exception:
            pass
        return None
    
    def _save_entity(self, scenario_id: str, entity_type: str, entity: Dict) -> str:
        """
        Save entity to scenario_entities table (and optionally to canonical table).
        
        Returns entity_id.
        """
        # Determine entity ID
        table_name, id_column = get_table_info(entity_type)
        entity_id = entity.get(id_column) or entity.get('id') or entity.get(f'{entity_type}_id') or str(uuid4())
        
        # Store full entity as JSON in scenario_entities
        entity_json = json.dumps(entity, default=str)
        
        # Check if entity already exists for this scenario
        existing = self.conn.execute("""
            SELECT id FROM scenario_entities 
            WHERE scenario_id = ? AND entity_type = ? AND entity_id = ?
        """, [scenario_id, entity_type, entity_id]).fetchone()
        
        if existing:
            # Update existing
            self.conn.execute("""
                UPDATE scenario_entities 
                SET entity_data = ?
                WHERE scenario_id = ? AND entity_type = ? AND entity_id = ?
            """, [entity_json, scenario_id, entity_type, entity_id])
        else:
            # Insert new (explicitly use sequence for id)
            self.conn.execute("""
                INSERT INTO scenario_entities (id, scenario_id, entity_type, entity_id, entity_data, created_at)
                VALUES (nextval('scenario_entities_seq'), ?, ?, ?, ?, ?)
            """, [scenario_id, entity_type, entity_id, entity_json, datetime.utcnow()])
        
        # Also try to insert into canonical table if serializer exists
        serializer = get_serializer(entity_type)
        if serializer:
            try:
                self._insert_canonical_entity(scenario_id, entity_type, entity, serializer)
            except Exception:
                # Canonical insert is optional - JSON storage is the primary
                pass
        
        return entity_id
    
    def _insert_canonical_entity(self, scenario_id: str, entity_type: str, entity: Dict, serializer) -> None:
        """Insert entity into canonical table using serializer."""
        table_name, id_column = get_table_info(entity_type)
        
        # Get provenance from entity
        provenance = entity.get('_provenance', {})
        if 'provenance' in entity:
            prov_data = entity['provenance']
            if isinstance(prov_data, dict):
                provenance = prov_data
        
        # Serialize entity
        data = serializer(entity, provenance)
        
        # Add scenario_id to data
        data['scenario_id'] = scenario_id
        
        # Build INSERT statement
        columns = list(data.keys())
        placeholders = ', '.join(['?' for _ in columns])
        
        # For conflict handling, update all columns except the primary key
        non_pk_columns = [c for c in columns if c != id_column]
        updates = ', '.join([f"{col} = excluded.{col}" for col in non_pk_columns])
        
        try:
            self.conn.execute(f"""
                INSERT INTO {table_name} ({', '.join(columns)})
                VALUES ({placeholders})
                ON CONFLICT ({id_column}) DO UPDATE SET {updates}
            """, list(data.values()))
        except Exception:
            # Table might not exist or columns might not match - this is OK
            pass
    
    def _load_scenario_entities(self, scenario_id: str) -> Dict[str, List[Dict]]:
        """Load all entities for a scenario from scenario_entities table."""
        results = self.conn.execute("""
            SELECT entity_type, entity_id, entity_data
            FROM scenario_entities
            WHERE scenario_id = ?
            ORDER BY entity_type, created_at
        """, [scenario_id]).fetchall()
        
        entities: Dict[str, List[Dict]] = {}
        for row in results:
            entity_type = row[0]
            entity_data = row[2]
            
            # Parse JSON
            if isinstance(entity_data, str):
                try:
                    entity = json.loads(entity_data)
                except json.JSONDecodeError:
                    entity = {'id': row[1], '_raw': entity_data}
            else:
                entity = entity_data if entity_data else {'id': row[1]}
            
            if entity_type not in entities:
                entities[entity_type] = []
            entities[entity_type].append(entity)
        
        return entities
    
    def _delete_scenario_entities(self, scenario_id: str) -> None:
        """Remove all entity links for a scenario."""
        self.conn.execute(
            "DELETE FROM scenario_entities WHERE scenario_id = ?",
            [scenario_id]
        )
    
    # =========================================================================
    # JSON Export/Import Methods
    # =========================================================================
    
    def export_to_json(
        self,
        name_or_id: str,
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        Export a scenario to JSON file for sharing.
        
        Args:
            name_or_id: Scenario name or UUID
            output_path: Where to save (default: ~/Downloads/{name}.json)
            
        Returns:
            Path to exported file
        """
        from .legacy import export_to_json as _export, export_scenario_for_sharing
        
        scenario = self.load_scenario(name_or_id)
        
        # Use default path if not specified
        if output_path is None:
            downloads = Path.home() / "Downloads"
            downloads.mkdir(exist_ok=True)
            # Clean name for filename
            safe_name = scenario['name'].replace(' ', '_').replace('/', '-')
            output_path = downloads / f"{safe_name}.json"
        
        # Prepare for export (remove internal fields)
        export_data = export_scenario_for_sharing(scenario)
        
        return _export(export_data, Path(output_path))
    
    def import_from_json(
        self,
        json_path: Path,
        name: Optional[str] = None,
        overwrite: bool = False,
    ) -> str:
        """
        Import a scenario from JSON file.
        
        Args:
            json_path: Path to JSON file
            name: Override scenario name (default: use filename or embedded name)
            overwrite: Replace existing scenario with same name
            
        Returns:
            Scenario ID
        """
        from .legacy import import_from_json as _import
        
        data = _import(Path(json_path))
        
        # Determine name (priority: argument > embedded > filename)
        scenario_name = name or data.get('name') or Path(json_path).stem
        
        # Get description and tags
        description = data.get('description')
        tags = data.get('tags', [])
        
        # Extract entities
        entities = data.get('entities', {})
        
        # Handle legacy format where entities are at top level
        if not entities:
            legacy_types = [
                'patients', 'patient',
                'encounters', 'encounter', 
                'diagnoses', 'diagnosis',
                'medications', 'medication',
                'members', 'member',
                'claims', 'claim',
                'prescriptions', 'prescription',
                'subjects', 'subject',
            ]
            for key in legacy_types:
                if key in data and isinstance(data[key], list):
                    # Normalize to plural form
                    normalized_key = key if key.endswith('s') else key + 's'
                    entities[normalized_key] = data[key]
        
        # Handle EntityWithProvenance wrapper format
        for entity_type in list(entities.keys()):
            entity_list = entities[entity_type]
            if entity_list and isinstance(entity_list[0], dict):
                if 'data' in entity_list[0] and 'provenance' in entity_list[0]:
                    # Unwrap EntityWithProvenance
                    entities[entity_type] = [
                        {**e['data'], '_provenance': e.get('provenance', {})}
                        for e in entity_list
                    ]
        
        return self.save_scenario(
            name=scenario_name,
            entities=entities,
            description=description,
            tags=tags,
            overwrite=overwrite,
        )


# =============================================================================
# Module-level convenience functions (for backward compatibility)
# =============================================================================

_manager: Optional[StateManager] = None


def get_manager() -> StateManager:
    """Get singleton state manager instance."""
    global _manager
    if _manager is None:
        _manager = StateManager()
    return _manager


def reset_manager() -> None:
    """Reset the singleton manager (for testing)."""
    global _manager
    _manager = None


def save_scenario(name: str, entities: Dict, **kwargs) -> str:
    """Convenience function for save_scenario."""
    return get_manager().save_scenario(name, entities, **kwargs)


def load_scenario(name_or_id: str) -> Dict:
    """Convenience function for load_scenario."""
    return get_manager().load_scenario(name_or_id)


def list_scenarios(**kwargs) -> List[Dict]:
    """Convenience function for list_scenarios."""
    return get_manager().list_scenarios(**kwargs)


def delete_scenario(name_or_id: str, confirm: bool = False) -> bool:
    """Convenience function for delete_scenario."""
    return get_manager().delete_scenario(name_or_id, confirm=confirm)


def scenario_exists(name_or_id: str) -> bool:
    """Convenience function for scenario_exists."""
    return get_manager().scenario_exists(name_or_id)


def export_scenario_to_json(name_or_id: str, output_path: Optional[Path] = None) -> Path:
    """Convenience function for export_to_json."""
    return get_manager().export_to_json(name_or_id, output_path)


def import_scenario_from_json(json_path: Path, name: Optional[str] = None, overwrite: bool = False) -> str:
    """Convenience function for import_from_json."""
    return get_manager().import_from_json(json_path, name, overwrite)


# New convenience functions for auto-persist pattern
def persist(entities: Dict[str, List[Dict]], **kwargs) -> PersistResult:
    """Convenience function for persist (auto-persist pattern)."""
    return get_manager().persist(entities, **kwargs)


def get_summary(scenario_id_or_name: str, **kwargs) -> ScenarioSummary:
    """Convenience function for get_summary."""
    return get_manager().get_summary(scenario_id_or_name, **kwargs)


def query_scenario(scenario_id_or_name: str, sql: str, **kwargs) -> QueryResult:
    """Convenience function for query."""
    return get_manager().query(scenario_id_or_name, sql, **kwargs)
