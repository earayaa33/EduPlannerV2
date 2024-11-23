#from rest_framework.permissions import BasePermission

#class administradorAcademico(BasePermission):

 #   def has_permission(self, request, view):
  #      return request.user.groups.filter(name='Administrador academico').exists()

#class usuarioComun(BasePermission):
    
  #  def has_permission(self, request, view):
   #     return request.method in ('GET', 'HEAD', 'OPTIONS')