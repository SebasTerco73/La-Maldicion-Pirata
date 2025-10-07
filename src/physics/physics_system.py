"""
Sistema de física del juego.
Maneja la gravedad y las colisiones.
"""
from typing import Any, List, Tuple
import pygame
from ..utils.constants import PHYSICS_CONFIG

class PhysicsEntity:
    """Interfaz para objetos que pueden ser afectados por la física."""
    def __init__(self):
        self.vel_y: float = 0
        self.on_ground: bool = False
        self.gravity_affected: bool = True
        self.collision_rect: pygame.Rect = None

    def apply_force(self, force_x: float, force_y: float) -> None:
        """Aplica una fuerza al objeto."""
        pass

class PhysicsSystem:
    """Sistema de física que maneja la gravedad y las colisiones."""
    def __init__(self, gravity: float = PHYSICS_CONFIG["gravity"]):
        self.gravity = gravity
        self.entities: List[PhysicsEntity] = []
        self.ground_y = PHYSICS_CONFIG["ground_y"]

    def add_entity(self, entity: PhysicsEntity) -> None:
        """Añade una entidad al sistema de física."""
        self.entities.append(entity)

    def remove_entity(self, entity: PhysicsEntity) -> None:
        """Elimina una entidad del sistema de física."""
        if entity in self.entities:
            self.entities.remove(entity)

    def apply_gravity(self, entity: PhysicsEntity) -> None:
        """
        Aplica gravedad a una entidad.
        
        Args:
            entity: Entidad a la que aplicar gravedad
        """
        if entity.gravity_affected and not entity.on_ground:
            entity.vel_y += self.gravity
            entity.rect.y += entity.vel_y

            # Colisión con el suelo
            if entity.rect.bottom >= self.ground_y:
                entity.rect.bottom = self.ground_y
                entity.vel_y = 0
                entity.on_ground = True

    def check_collision(self, entity1: PhysicsEntity, entity2: PhysicsEntity) -> bool:
        """
        Comprueba si hay colisión entre dos entidades.
        
        Args:
            entity1: Primera entidad
            entity2: Segunda entidad
            
        Returns:
            bool: True si hay colisión, False en caso contrario
        """
        return entity1.collision_rect.colliderect(entity2.collision_rect)

    def update(self, dt: float) -> None:
        """
        Actualiza la física para todas las entidades.
        
        Args:
            dt: Delta time (tiempo transcurrido desde el último frame)
        """
        for entity in self.entities:
            if entity.gravity_affected:
                self.apply_gravity(entity)

class CollisionSystem:
    """Sistema de detección y resolución de colisiones."""
    def __init__(self):
        self.collidable_entities: List[PhysicsEntity] = []

    def add_collidable(self, entity: PhysicsEntity) -> None:
        """Añade una entidad al sistema de colisiones."""
        self.collidable_entities.append(entity)

    def remove_collidable(self, entity: PhysicsEntity) -> None:
        """Elimina una entidad del sistema de colisiones."""
        if entity in self.collidable_entities:
            self.collidable_entities.remove(entity)

    def check_collisions(self) -> List[Tuple[PhysicsEntity, PhysicsEntity]]:
        """
        Comprueba todas las colisiones entre entidades.
        
        Returns:
            Lista de tuplas con las entidades que colisionan
        """
        collisions = []
        for i, entity1 in enumerate(self.collidable_entities):
            for entity2 in self.collidable_entities[i + 1:]:
                if entity1.collision_rect.colliderect(entity2.collision_rect):
                    collisions.append((entity1, entity2))
        return collisions