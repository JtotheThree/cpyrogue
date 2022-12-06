# Modified from https://github.com/benmoran56/esper/
import time as _time
from functools import lru_cache as _lru_cache
from typing import List, Type, TypeVar, Any, Tuple, Iterable

C = TypeVar('C')
P = TypeVar('P')


class Processor:
    world = None

    def process(self, *args, **kwargs):
        raise NotImplementedError


class Event:
    def __init__(self, name, data, sender=None):
        self.name = name
        self.data = data
        self.sender = sender


class Component:
    def __init__(self):
        self.entity = None
        self.world = None

    def send(self, event, data):
        try:
            self.world.send(event, data, sender=self.entity)
        except KeyError:
            print("Error: No components exist with {} event.".format(event))

    def send_to_entity(self, entity, event, data):
        self.world.send_to_entity(entity, event, data, sender=self.entity)



class World:
    def __init__(self, timed=False):
        self._processors = []
        self._next_entity_id = 0
        self._components = {}
        self._entities = {}
        self._events = {}
        self._dead_entities = set()
        
        if timed:
            self.process_times = {}
            self._process = self._timed_process

    def clear_cache(self) -> None:
        self.get_component.cache_clear()
        self.get_components.cache_clear()

    def clear_database(self) -> None:
        """Remove all Entities and Components from the World."""
        self._next_entity_id = 0
        self._dead_entities.clear()
        self._components.clear()
        self._entities.clear()
        self.clear_cache()

    def add_processor(self, processor_instance: Processor, priority=0) -> None:
        assert issubclass(processor_instance.__class__, Processor)
        processor_instance.priority = priority
        processor_instance.world = self
        self._processors.append(processor_instance)
        self._processors.sort(key=lambda proc: proc.priority, reverse=True)

    def remove_processor(self, processor_type: Processor) -> None:
        for processor in self._processors:
            if type(processor) == processor_type:
                processor.world = None
                self._processors.remove(processor)

    def get_processor(self, processor_type: Type[P]) -> P:
        for processor in self._processors:
            if type(processor) == processor_type:
                return processor

    def create_entity(self, *components) -> int:
        self._next_entity_id += 1

        for component in components:
            self.add_component(self._next_entity_id, component)

        # self.clear_cache()
        return self._next_entity_id

    def delete_entity(self, entity, immediate=False) -> None:
        if immediate:
            for component_type in self._entities[entity]:
                self._components[component_type].discard(entity)

                if not self._components[component_type]:
                    del self._components[component_type]

            del self._entities[entity]
            self.clear_cache()

        else:
            self._dead_entities.add(entity)

    def component_for_entity(self, entity: int, component_type: Type[C]) -> C:
        return self._entities[entity][component_type]

    def components_for_entity(self, entity: int) -> Tuple[C, ...]:
        return tuple(self._entities[entity].values())

    def has_component(self, entity: int, component_type: Any) -> bool:
        return component_type in self._entities[entity]

    def add_component(self, entity: int, component_instance: Any) -> None:
        component_instance.entity = entity
        component_instance.world = self

        component_type = type(component_instance)

        if component_type not in self._components:
            self._components[component_type] = set()

        self._components[component_type].add(entity)

        if entity not in self._entities:
            self._entities[entity] = {}

        for event in component_instance.events:

            if event not in self._events:
                self._events[event] = set()

            self._events[event].add(component_type)

        self._entities[entity][component_type] = component_instance
        self.clear_cache()

    def remove_component(self, entity: int, component_type: Any) -> int:
        self._components[component_type].discard(entity)

        if not self._components[component_type]:
            del self._components[component_type]

        del self._entities[entity][component_type]

        if not self._entities[entity]:
            del self._entities[entity]

        self.clear_cache()
        return entity

    def _get_component(self, component_type: Type[C]) -> Iterable[Tuple[int, C]]:
        entity_db = self._entities

        for entity in self._components.get(component_type, []):
            yield entity, entity_db[entity][component_type]

    def _get_components(self, *component_types: Type) -> Iterable[Tuple[int, ...]]:
        entity_db = self._entities
        comp_db = self._components

        try:
            for entity in set.intersection(*[comp_db[ct]
                                             for ct in component_types]):
                yield entity, [entity_db[entity][ct] for ct in component_types]
        except KeyError:
            pass

    @_lru_cache()
    def get_component(self, component_type: Type[C]) -> List[Tuple[int, C]]:
        return [query for query in self._get_component(component_type)]

    @_lru_cache()
    def get_components(self, *component_types: Type):
        return [query for query in self._get_components(*component_types)]

    def try_component(self, entity: int, component_type: Type):
        if component_type in self._entities[entity]:
            yield self._entities[entity][component_type]
        else:
            return None

    def _clear_dead_entities(self):
        for entity in self._dead_entities:
            for component_type in self._entities[entity]:
                self._components[component_type].discard(entity)

                if not self._components[component_type]:
                    del self._components[component_type]
                
            del self._entities[entity]
    
        self._dead_entities.clear()
        self.clear_cache()

    def _process(self, *args, **kwargs):
        for processor in self._processors:
            processor.process(*args, **kwargs)

    def _timed_process(self, *args, **kwargs):
        for processor in self._processors:
            start_time = _time.process_time()
            processor.process(*args, **kwargs)
            process_time = int(round((_time.process_time() - start_time) * 1000, 2))
            self.process_times[processor.__class__.__name__] = process_time        

    def process(self, *args, **kwargs):
        self._clear_dead_entities()
        self._process(*args, **kwargs)

    def send_to_entity(self, entity, name, data, sender=None):
        entity_db = self._entities
        event_db = self._events

        if name not in event_db:
            return

        event = Event(name, data, sender)

        for component_instance in set.intersection(event_db[name],
                                                   entity_db[entity]):
            component = self._entities[entity][component_instance]
            call = getattr(component, name)
            event = call(event)

    def send(self, name, data, sender=None):
        event_db = self._events

        event = Event(name, data, sender)

        for component_instance in event_db[name]:
            for ent, component in self.get_component(component_instance):
                call = getattr(component, name)
                event = call(event)

    def print_events(self):
        for event in self._events.items():
            print(event)

    def print_entities(self):
        for entity in self._entities.items():
            print(entity)

    def print_components(self):
        for component in self._components.items():
            print(component)
