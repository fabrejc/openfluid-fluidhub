
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import unittest
import os

import TestsHelpers as helpers


################################################################################
################################################################################


class tests_APIWaresCreate(unittest.TestCase):

  @classmethod
  def setUpClass(cls):

    cls.Token = helpers.askForToken("admin","admin")


  def setUp(self):
    pass


################################################################################
################################################################################


  def createWare(self,Type,ID) :

    URL = "http://%s/api/wares/%s/%s" % (helpers.FluidhubAddr,Type,ID)
    Headers = {
     'content-type': "application/json",
     'authorization': "JWT %s" % self.Token,
     'cache-control': "no-cache",
    }

    with open(os.path.join(helpers.TestsPath,"definitions",ID+".json")) as DefFile :
      Payload = DefFile.read()
      Response = helpers.executePutRequest(URL, Data=Payload, Headers=Headers)
      helpers.printResponse(Response)
      return Response


################################################################################


  def getWare(self,Type,ID) :

    URL = "http://%s/api/wares/%s/%s" % (helpers.FluidhubAddr,Type,ID)

    Response = helpers.executeGetRequest(URL)
    helpers.printResponse(Response)
    return Response



################################################################################


  def getWares(self,Type,Username=None) :

    UserArg = ""
    if Username :
      UserArg = "?username=%s" % Username

    URL = "http://%s/api/wares/%s%s" % (helpers.FluidhubAddr,Type,UserArg)

    Response = helpers.executeGetRequest(URL)
    helpers.printResponse(Response)
    return Response


################################################################################
################################################################################


  def test01_CreateWares(self):
    for Type, IDs in helpers.Wares.iteritems():
      for ID in IDs:
        Response = self.createWare(Type,ID)
        self.assertEqual(Response.status_code,201)


################################################################################


  def test10_GetWares(self):

    for Type, IDs in helpers.Wares.iteritems():
      for ID in IDs:
        Response = self.getWare(Type,ID)
        self.assertEqual(Response.status_code,200)
      Response = self.getWares(Type)
      self.assertEqual(Response.status_code,200)
      Response = self.getWares(Type,"admin")
      self.assertEqual(Response.status_code,200)


################################################################################


  def test11_GetAllWares(self):
    Response = helpers.executeGetRequest("http://%s/api/wares" % (helpers.FluidhubAddr))
    helpers.printResponse(Response)
    self.assertEqual(Response.status_code,200)


################################################################################
################################################################################


if __name__ == '__main__':
    unittest.main()
