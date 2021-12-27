from wagtail.core import hooks
from django.utils.crypto import get_random_string
from wagtail.core.models import Page
import graphene
import json


from grapple.types.pages import PageInterface
from website.models import ArticlePage

from wagtail.core.fields import StreamField
from wagtail.core import blocks

        
class CreateArticlePage(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        parent = graphene.Int()
        date_display = graphene.String()
        slug = graphene.String()
        body = graphene.String()
        #body = graphene.JSONString()

    ok = graphene.Boolean()
    article = graphene.Field(
        PageInterface,
    )
    

    def mutate(root, info, title, parent, body, date_display, slug):
        # We use uuid here in order to ensure the slug will always be unique accross tests
        

        #body=json.dumps([
        #    {'type':'text', 'value': '##␣New Heading'},
        #    {'type':'text', 'value': '## New Heading \ 23232'},
        #    {'type':'html', 'value': '<strong>My Paragraph</strong>'},])
        
        article = ArticlePage(title=title, date_display=date_display,slug=slug,body=body, live=False)
        ok = True
        Page.objects.get(id=parent).add_child(instance=article)
        #article.save_revision().publish()
        article.save_revision()
        return CreateArticlePage(article=article, ok=ok)        


class Mutations(graphene.ObjectType):
    #create_author = CreateAuthor.Field()
    create_article = CreateArticlePage.Field()
    

#### GRAPHQL mutation: ###

#mutation myFirstMutation {
#    createArticle(
#      title:"Once upon a time 8", 
#      parent:12, 
#      dateDisplay:"2021-11-21",
#      slug:"abc8") {
#        article {
#            title,
#        }
#        ok
#    }
#}    
